import random

from messenger import intents
from messenger.api.formatters import format_text, format_generic_simple
from messenger.formatters.general import format_quick_reply_with_intent
from messenger.formatters.generic_quiz import format_quiz_question, format_yes_or_no_question
from messenger.formatters.party_quiz import format_quiz_result_reply
from messenger.formatters.voter_guide import format_quiz_result_button
from messenger.utils import get_next_manuscript
from quiz.models import QuizAlternative, QuizAnswer, Manuscript


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


def get_quiz_completed_replies(sender_id, session):
    extra_payload = {'manuscript': Manuscript.objects.get_default(default=Manuscript.DEFAULT_QUIZ).pk}
    msg = 'Se svarene i detalj på din egen resultatside'
    ready_msg = 'Klar for å gå videre?'
    image_url = 'https://data.holderdeord.no/assets/og_logo-8b1cb2e26b510ee498ed698c4e9992df.png'

    return [
        format_text(sender_id, 'Gratulerer 👏👏👏 Du har fullført quizen!'),
        format_quiz_result_reply(sender_id, session),
        format_generic_simple(sender_id, msg, format_quiz_result_button(session), image_url=image_url),
        format_quick_reply_with_intent(sender_id, 'Videre', ready_msg, intents.INTENT_RESET_SESSION, extra_payload)]


def get_generic_quiz_answer_replies(sender_id, session, payload, answer: QuizAnswer):
    try:
        alt = QuizAlternative.objects.get(pk=payload['alternative'])
    except QuizAlternative.DoesNotExist:
        return []

    next_text = _get_next_text(alt)

    next_manuscript = get_next_manuscript(session, quiz=True)
    if next_manuscript:
        session.meta['next_manuscript'] = next_manuscript.pk if next_manuscript else None
        return [format_text(sender_id, next_text)]

    # Emptied out quiz
    return get_quiz_completed_replies(sender_id, session)
