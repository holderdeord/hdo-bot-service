from pprint import pprint
from random import randint

import requests
from django.conf import settings
from django.db.models import Count

from messenger.models import ChatSession
from quiz.models import GoogleProfile, AnswerSet, Answer, Promise, Party


def get_google_sheet_data():
    """ Ref: https://github.com/google/oauth2client/blob/master/oauth2client/contrib/django_util/__init__.py#L188
        Ref: https://github.com/google/oauth2client/tree/master/samples/django/django_user
    """
    access_token = get_google_access_token()
    if not access_token:
        return []

    params = {
        'access_token': access_token
    }
    url = 'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/promises'.format(
        spreadsheet_id=settings.GOOGLE_SPREADSHEET_ID)
    res = requests.get(url, params).json()

    if res.get('error') and res['error']['code'] == 401:
        # Reset access_token
        GoogleProfile.objects.all().delete()
        return []

    return res.get('values')


def get_google_access_token():
    gp = GoogleProfile.objects.first()
    return gp.credential.access_token if gp else None


def get_promise_id(promise_document):
    return promise_document['_links']['self']['href'].split('/')[-1]


def _promises_as_dict(promise_list):
    return {str(p['pk']): p['status'] for p in promise_list}


def save_answers(chat_session: ChatSession):
    """ When all questions have been answered in a session create answer objects. """
    answer_data = chat_session.meta.get('answers')
    if not answer_data:
        return

    if AnswerSet.objects.filter(session=chat_session).exists():
        return

    promises = _promises_as_dict(chat_session.meta['manuscript']['promises'])

    answer_set = AnswerSet.objects.create(session=chat_session)
    for promise_id, status in answer_data.items():
        pprint(promises)
        pprint(promise_id)
        Answer.objects.create(
            promise_id=promise_id,
            status=status,
            answer_set=answer_set,
            correct_status=promises[str(promise_id)] == status)


def format_question(promise: Promise, question_type='checked'):
    # TODO: You are here
    if question_type == 'checked':
        return {
            'possible': [promise.FULFILLED, promise.BROKEN],
            'answer': promise.status
        }
    elif question_type == 'a_or_b':
        right = promise.parties.first()

        wrong_parties = Party.objects.filter(pk=right.pk)
        count = wrong_parties.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        wrong = wrong_parties[random_index]

        return {
            'possible': [right, wrong],
            'answer': right
        }
    elif question_type == 'true_or_false':
        return {
            'possible': [True, False],
            'answer': promise
        }
