import random

from messenger import intents
from messenger.api.formatters import format_text, format_generic_simple
from messenger.formatters.general import format_quick_reply_with_intent
from messenger.formatters.generic_quiz import format_quiz_question, format_yes_or_no_question
from messenger.formatters.party_quiz import format_quiz_result_reply
from messenger.formatters.voter_guide import format_quiz_result_button
from messenger.utils import get_next_manuscript, get_answered_manuscripts, get_unanswered_manuscripts
from quiz.models import QuizAlternative, Manuscript


def get_quiz_question_replies(sender_id, session, payload):
    """ Show question for given manuscript item """
    return [format_quiz_question(sender_id, session.meta['manuscript'])]


def get_yes_or_no_question_replies(sender_id, session, payload):
    """ Show question for given manuscript item """
    return [format_yes_or_no_question(sender_id, session.meta['manuscript'])]


def _get_next_text(alt):
    positive_emojis = ['👍', '😃', '👌', '❤', '👏', '💪', '👊']
    negative_emojis = ['💩']
    if alt.correct_answer:
        return 'Riktig! {}'.format(random.choice(positive_emojis))

    correct_alt = alt.get_correct_in_same_manuscript()
    correct_text = ''
    if correct_alt:
        correct_text = ' Riktig svar er {}'.format(correct_alt.text)

    return 'Feil {}{}'.format(random.choice(negative_emojis), correct_text)


def get_quiz_result_replies(sender_id, session, quiz_completed=False):
    msg = 'Se svarene i detalj på din egen resultatside'
    image_url = 'https://data.holderdeord.no/assets/og_logo-8b1cb2e26b510ee498ed698c4e9992df.png'

    replies = []

    if quiz_completed:
        replies += [format_text(sender_id, 'Gratulerer 👏👏👏 Du har fullført quizen!')]

        ready_msg = 'Vil du prøve på nytt?'
        next_action = format_quick_reply_with_intent(
            sender_id, 'Start på nytt', ready_msg, intents.INTENT_RESET_ANSWERS_CONFIRM_SILENT)
    else:
        ready_msg = 'Klar for å gå videre?'
        extra_payload = {'manuscript': Manuscript.objects.get_default(default=Manuscript.DEFAULT_QUIZ).pk}
        next_action = format_quick_reply_with_intent(
            sender_id, 'Videre', ready_msg, intents.INTENT_RESET_SESSION, extra_payload)

    return replies + [
        format_quiz_result_reply(sender_id, session),
        format_generic_simple(sender_id, msg, format_quiz_result_button(session), image_url=image_url),
        next_action]


def _is_half_way_in_quiz(session):
    answered = get_answered_manuscripts(session).count()
    unanswered = get_unanswered_manuscripts(session, quiz=True).count()
    return answered - 1 == unanswered or answered == unanswered


def get_generic_quiz_answer_replies(sender_id, session, payload):
    try:
        alt = QuizAlternative.objects.get(pk=payload['alternative'])
    except QuizAlternative.DoesNotExist:
        return []

    next_text = _get_next_text(alt)

    if _is_half_way_in_quiz(session):
        replies = [format_text(sender_id, next_text)]
        return replies + get_quiz_result_replies(sender_id, session)

    next_manuscript = get_next_manuscript(session, quiz=True)
    if next_manuscript:
        session.meta['next_manuscript'] = next_manuscript.pk if next_manuscript else None
        return [format_text(sender_id, next_text)]

    # Emptied out quiz
    replies = [format_text(sender_id, next_text)]
    return replies + get_quiz_result_replies(sender_id, session, quiz_completed=True)


def get_initial_quiz_question_reply(sender_id, session, payload, item):
    """ Show initial question """
    next_manuscript = get_next_manuscript(session, quiz=True)
    if next_manuscript:
        session.meta['next_manuscript'] = next_manuscript.pk if next_manuscript else None
        return []  # No replies, should loop to next manuscript

    # Emptied out quiz
    replies = [format_text(sender_id, 'Finner ingen flere spørsmål 👏👏👏 Du har fullført quizen!')]
    return replies + get_quiz_result_replies(sender_id, session, quiz_completed=True)
