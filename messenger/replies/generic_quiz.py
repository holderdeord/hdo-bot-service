import random

from messenger import intents
from messenger.api.formatters import format_text
from messenger.formatters.generic_quiz import format_quiz_question, format_yes_or_no_question
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
    replies = [
        format_text(sender_id, next_text),
        format_text(sender_id, 'Du runna quizen, hurra!')
    ]

    return replies
