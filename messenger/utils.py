import json

from rest_framework.renderers import JSONRenderer

from api.serializers.manuscript import BaseManuscriptSerializer
from messenger.api import send_message
from messenger.api.formatters import format_text
from messenger.models import ChatSession
from quiz.models import AnswerSet, Answer, Manuscript


def render_and_load_manuscript(manuscript):
    return json.loads(JSONRenderer().render(BaseManuscriptSerializer(manuscript).data).decode())


def init_or_reset_session(sender_id, session=None, manuscript_pk=None):
    if manuscript_pk is None:
        manuscript = Manuscript.objects.get_default()
    else:
        manuscript = Manuscript.objects.get(pk=manuscript_pk)

    if not manuscript:
        msg = "No manuscripts, bailing..."
        send_message(format_text(sender_id, msg))
        raise Exception(msg)

    # Serialize what we need and put in the session state
    meta = {
        'manuscript': render_and_load_manuscript(manuscript),
        'item': 0,
        'promise': 0,
        'first_name': ''
    }

    # Existing?
    if session is not None:
        session.meta = meta
        session.save()
        return session

    return ChatSession.objects.create(user_id=sender_id, meta=meta)


def _promises_as_dict(promise_list):
    return {str(p['pk']): p['status'] for p in promise_list}


def save_answers(chat_session: ChatSession):
    """ When all questions have been answered in a manuscript create answer objects. """
    answer_data = chat_session.meta.get('answers')
    if not answer_data:
        return

    if AnswerSet.objects.filter(session=chat_session).exists():
        return

    promises = _promises_as_dict(chat_session.meta['manuscript']['promises'])

    answer_set = AnswerSet.objects.create(session=chat_session)
    for promise_id, status in answer_data.items():
        Answer.objects.create(
            promise_id=promise_id,
            status=status,
            answer_set=answer_set,
            correct_status=promises[str(promise_id)] == status)
