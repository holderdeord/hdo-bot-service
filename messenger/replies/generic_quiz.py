import random

from messenger import intents
from messenger.api.formatters import format_text
from messenger.formatters.generic_quiz import format_quiz_alternatives
from messenger.utils import get_next_manuscript
from quiz.models import QuizAlternative, QuizAnswer, Manuscript


def get_quiz_question_replies(sender_id, session, payload):
    """ Show question for given manuscript item """
    return [format_quiz_alternatives(sender_id, session.meta['manuscript'])]


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
    # extra_payload = {'manuscript': Manuscript.objects.get_default(default=Manuscript.DEFAULT_QUIZ).pk}
    # num_completed_categories = len(completed_categories(session, quiz=True))
    replies = []
    # if num_completed_questions == 10:
    #     # We collect your answers, show results
    #     finished_msg = 'Spørsmålene du får er hentet fra Holder de ord sine tjenester.'
    #     result_page_msg = 'Se svarene i detalj og hvilke løfter som hører til på din egen resultatside'
    #     more_cats_msg = 'Du kan se svarene dine fra menyen når som helst.'
    #     image_url = 'https://data.holderdeord.no/assets/og_logo-8b1cb2e26b510ee498ed698c4e9992df.png'
    #     replies += [
    #         format_text(sender_id, next_text),
    #         format_quiz_result_reply(sender_id, session),
    #         format_text(sender_id, finished_msg),
    #         format_generic_simple(sender_id, result_page_msg, format_quiz_result_button(session), image_url=image_url),
    #         format_quick_reply_with_intent(
    #             sender_id, 'Neste tema!', more_cats_msg, intents.INTENT_NEXT_QUESTION, extra_payload)]
    # else:
    #     # Next manuscript
    #     replies += [
    #         format_quick_reply_with_intent(
    #             sender_id, 'Neste tema!', next_text, intents.INTENT_NEXT_QUESTION, extra_payload)
    #     ]

    replies += [
        format_text(sender_id, next_text),
        format_text(sender_id, 'Du runna quizen, hurra!')
    ]

    return replies
