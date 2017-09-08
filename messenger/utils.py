import json

import logging
from collections import defaultdict, OrderedDict
from django.conf import settings
from django.db import connection
from django.db.models import Case, When, Func
from django.urls import reverse
from rest_framework.renderers import JSONRenderer

from api.serializers.manuscript import BaseManuscriptSerializer
from messenger.api import send_message
from messenger.api.formatters import format_text
from messenger.models import ChatSession
from quiz.models import AnswerSet, Answer, Manuscript, VoterGuideAlternative, VoterGuideAnswer, QuizAnswer, \
    QuizAlternative

logger = logging.getLogger(__name__)


def render_and_load_manuscript(manuscript):
    return json.loads(JSONRenderer().render(BaseManuscriptSerializer(manuscript).data).decode())


def order_field_nb_no(field_name):
    if connection.vendor == 'sqlite':
        return field_name

    return Func(
        field_name,
        function='nb_NO',
        template='(%(expressions)s) COLLATE "%(function)s"')


def init_or_reset_session(sender_id, session=None, manuscript_pk=None):
    default_manuscript = Manuscript.objects.get_default()
    if manuscript_pk is None:
        manuscript = default_manuscript
    else:
        try:
            manuscript = Manuscript.objects.get(pk=manuscript_pk)
        except Manuscript.DoesNotExist:
            logger.warning("Session referenced non-existing manuscript={}".format(manuscript_pk))
            manuscript = default_manuscript

    if not default_manuscript:
        if settings.DEBUG:
            send_message(format_text(sender_id, "No manuscripts, bailing..."))

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


def delete_answers(session: ChatSession):
    AnswerSet.objects.filter(session=session).delete()
    # Also reset session
    session.meta['next_manuscript'] = Manuscript.objects.get_default().pk


def save_vg_answer(session: ChatSession, payload):
    try:
        alt = VoterGuideAlternative.objects.get(pk=payload['alternative'])
    except VoterGuideAlternative.DoesNotExist:
        return

    answer_set, _ = AnswerSet.objects.get_or_create(session=session)  # reuse answerset
    answer, _ = VoterGuideAnswer.objects.get_or_create(answer_set=answer_set, voter_guide_alternative=alt)


def save_quiz_answer(session: ChatSession, payload):
    try:
        alt = QuizAlternative.objects.get(pk=payload['alternative'])
    except QuizAlternative.DoesNotExist:
        return

    answer_set, _ = AnswerSet.objects.get_or_create(session=session)  # reuse answerset
    answer, _ = QuizAnswer.objects.get_or_create(answer_set=answer_set, quiz_alternative=alt)

    return answer


def get_unanswered_manuscripts(session: ChatSession, selection=None, quiz=False, level=None):
    query = {
        'active': True,
        'type': Manuscript.TYPE_VOTER_GUIDE
    }
    if quiz:
        query['type'] = Manuscript.TYPE_QUIZ
        if level:
            query['level'] = level

    ms = Manuscript.objects.filter(**query)

    if selection:
        ms = ms.filter(pk__in=selection)

    if quiz:
        answers = QuizAnswer.objects.filter(answer_set__session=session)
        return ms.exclude(quiz_alternatives__answers__in=answers)

    answers = VoterGuideAnswer.objects.filter(answer_set__session=session)
    return ms.exclude(voter_guide_alternatives__answers__in=answers)


def get_next_manuscript(session: ChatSession, quiz=False):
    ms = get_unanswered_manuscripts(session, quiz=quiz)
    current_category = session.meta['manuscript']['hdo_category']
    return ms.filter(hdo_category=current_category).order_by('?').first()


def completed_categories(session, quiz=False):
    if quiz:
        manuscripts = Manuscript.objects.filter(quiz_alternatives__answers__answer_set__session=session)
    else:
        manuscripts = Manuscript.objects.filter(voter_guide_alternatives__answers__answer_set__session=session)

    return set(manuscripts.values_list('hdo_category', flat=True))


def get_manuscripts_for_category_selection(session: ChatSession, selection=None, quiz=False, level=None):
    """ Get voter guide manuscripts that are not already answered, max 1 per HDO category """

    # Remove manuscripts already answered
    manuscripts = get_unanswered_manuscripts(session, selection, quiz=quiz, level=level)

    # Randomize
    manuscripts = manuscripts.order_by('?')

    # Make manuscripts unique per HDO category
    # Note: Iterating over the queryset evaluates it and lets us sort it by name again later
    exclude_manuscripts = []
    seen_cats = []
    for m in manuscripts:
        if m.hdo_category.pk not in seen_cats:
            seen_cats.append(m.hdo_category.pk)
        else:
            exclude_manuscripts.append(m.pk)

    manuscripts = manuscripts.exclude(pk__in=exclude_manuscripts)

    if selection:
        # Keep manuscript selection order
        manuscripts = manuscripts.order_by(Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(selection)]))
    else:

        manuscripts = manuscripts.order_by(order_field_nb_no('hdo_category__name'))

    manuscripts = manuscripts.select_related('hdo_category')
    return manuscripts


def get_quiz_answer_set_url(session: ChatSession):
    url = reverse('quiz:quiz-answer-set-detail', args=[session.answers.uuid])
    return '{}{}'.format(settings.BASE_URL, url)


def get_messenger_bot_url():
    return 'https://m.me/{}'.format(settings.FACEBOOK_PAGE_ID)


def count_and_sort_answers(alts):
    # Note: Each alternative can have more than 1 promise tied to the same party
    parties_by_alternative = defaultdict(set)
    for alt in alts.all():
        for p in alt.promises.all():
            parties_by_alternative[alt.pk].add(p.promisor_name)

    # Count and sort number of answers by party
    counts = defaultdict(lambda: 0)
    for alt, parties in parties_by_alternative.items():
        for p in parties:
            counts[p] += 1
    ordered_counts = OrderedDict(sorted(counts.items(), key=lambda c: c[1], reverse=True))

    # Group by counts
    grouped_by_counts = OrderedDict()
    for party, count in ordered_counts.items():
        if count in grouped_by_counts:
            grouped_by_counts[count] += [party]
        else:
            grouped_by_counts[count] = [party]

    return grouped_by_counts


def populate_categories(answered_alts):
    categories = sorted(set([alt.manuscript.hdo_category for alt in answered_alts]), key=lambda x:x.name)
    for category in categories:
        category.correct = answered_alts.filter(manuscript__hdo_category=category).filter(correct_answer=True).count()
        category.total = answered_alts.filter(manuscript__hdo_category=category).count()
    return categories


def populate_questions_and_alternatives(answered_alts, all_alts):
    questions = [alternative.manuscript for alternative in answered_alts]

    for question in questions:
        question.alternatives = all_alts.filter(manuscript=question)
        question.answered = answered_alts.filter(manuscript=question)
        question.answered_text = join_querysets(question.answered, 'text')
        question.correct_alts = question.alternatives.filter(correct_answer=True)
        question.correct_alts_text = join_querysets(question.correct_alts, 'text')
        question.correct = True
        for answer in question.answered:
            question.correct = question.correct and question.correct_alts.filter(pk=answer.pk).count() > 0
        question.table_class = "table-success" if question.correct else "table-danger"

    return questions


def join_querysets(set, attribute):
    return ', '.join([item[attribute] for item in set.values()])
