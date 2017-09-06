import json
import random

from django.utils.translation import ugettext as _

from messenger import intents
from messenger.api import get_user_profile
from messenger.api.formatters import format_text, format_image_attachment, format_quick_replies, format_generic_simple
from messenger.formatters.general import format_quick_reply_with_intent
from messenger.formatters.quiz import format_quiz_alternatives, format_quiz_answer_button
from messenger.utils import save_answers, get_next_manuscript

from quiz.models import Manuscript, QuizAlternative, QuizAnswer
from quiz.utils import PARTY_SHORT_NAMES


def get_quiz_level_replies(sender_id, session, payload, text):
    """ Show available skill levels as quick replies """
    buttons = []
    for val, level in Manuscript.LEVEL_CHOICES:
        buttons.append({
            "content_type": "text",
            "title": str(level),
            "payload": json.dumps({
                'level': val,
                'intent': intents.INTENT_NEXT_ITEM
            }),
        })

    return [format_quick_replies(sender_id, buttons, text)]


def get_quiz_question_replies(sender_id, session, payload):
    """ Show question for given category"""
    return [format_quiz_alternatives(sender_id, session.meta['manuscript'])]


def _get_correct_alt(alt):
    return QuizAlternative.objects.filter(manuscript=alt.manuscript, correct_answer=True).first()


def _get_next_text(alt):
    positive_emojis = ['👍', '😃', '👌', '❤', '👏', '💪', '👊']
    negative_emojis = ['💩']
    if alt.correct_answer:
        return 'Riktig! {}'.format(random.choice(positive_emojis))

    correct_alt = _get_correct_alt(alt)
    correct_text = ''
    if correct_alt:
        correct_text = ' Riktig svar er {}'.format(PARTY_SHORT_NAMES[correct_alt.text])

    return 'Feil {}{}'.format(random.choice(negative_emojis), correct_text)


def get_quiz_answer_replies(sender_id, session, payload, answer: QuizAnswer):
    try:
        alt = QuizAlternative.objects.get(pk=payload['alternative'])
    except QuizAlternative.DoesNotExist:
        return []

    next_text = _get_next_text(alt)

    next_manuscript = get_next_manuscript(session, quiz=True)
    if next_manuscript:
        session.meta['next_manuscript'] = next_manuscript.pk if next_manuscript else None
        return [
            format_text(sender_id, next_text),
            format_generic_simple(
                sender_id,
                'Vil du se svar i detalj?',
                format_quiz_answer_button(answer)),

        ]

    # Emptied out the category, link manuscript select
    extra_payload = {'manuscript': Manuscript.objects.get_default(default=Manuscript.DEFAULT_QUIZ).pk}
    num_answers = QuizAnswer.objects.filter(answer_set__session=session).count()
    replies = []

    # FIXME: This needs to look at completed category or not
    # if 4 <= num_answers < 8:
    #     # Intro to bot
    #     finished_msg = 'Du har nå gått gjennom alle spørsmålene med dette temaet.'
    #     about_bot_text = 'Spørsmålene du får er hentet fra vår løftebase som inneholder alle partiprogrammene.'
    #     replies += [
    #         format_text(sender_id, next_text), format_text(sender_id, finished_msg),
    #         format_quick_reply_with_intent(
    #             sender_id, 'Neste tema!', about_bot_text, intents.INTENT_NEXT_QUESTION, extra_payload)]
    #
    # elif 8 <= num_answers < 12:
    #     # We collect your answers, show results
    #     result_page_msg = 'Se svarene i detalj og hvilke løfter som hører til på din egen resultatside'
    #     more_cats_msg = 'Du kan se svarene dine fra menyen når som helst. Velg nytt tema for å gjøre ditt resultat mer presist.'
    #     image_url = 'https://data.holderdeord.no/assets/og_logo-8b1cb2e26b510ee498ed698c4e9992df.png'
    #     replies += [
    #         format_text(sender_id, next_text),
    #         format_vg_result_reply(sender_id, session),
    #         format_generic_simple(sender_id, result_page_msg, format_vg_result_button(session),
    #                               image_url=image_url),
    #         format_quick_reply_with_intent(
    #             sender_id, 'Neste tema!', more_cats_msg, intents.INTENT_NEXT_QUESTION, extra_payload)]
    # else:
    # Next manuscript
    replies += [
        format_quick_reply_with_intent(sender_id, 'Neste tema!', next_text, intents.INTENT_NEXT_QUESTION, extra_payload)
    ]

    return replies


def get_quiz_broken_question_replies(sender_id, session, payload=None):
    """ Get replies to quiz answers INTENT_ANSWER_QUIZ_QUESTION """
    first_name = session.meta['first_name']
    if not first_name:
        first_name = session.meta['first_name'] = get_user_profile(sender_id)['first_name']

    # Get last asked promise
    p_i = session.meta['promise']
    if p_i > 0:
        p_i -= 1
    promise = session.meta['manuscript']['promises'][p_i]

    # Is answer correct?
    if payload['answer'] == promise['status']:
        text = 'Godt svar {} 🙂 Det løftet ble {}'.format(first_name, _(promise['status']))
    else:
        text = 'Beklager {} 😩  Det var ikke riktig, det løftet ble {}'.format(first_name, _(promise['status']))

    replies = [format_text(sender_id, text)]

    # Try to get a random image of correct type and display 1 out of 3 times
    images = list(filter(lambda x: x['type'] == promise['status'], session.meta['manuscript']['images']))
    if images and session.meta['promise'] % 3 == 0:
        image = random.choice(images)
        replies += [format_image_attachment(sender_id, image['url'])]

    # Is last promise?
    if session.meta['promise'] == len(session.meta['manuscript']['promises']):
        save_answers(session)

    # Update answer state
    current_answers = session.meta.get('answers', {})
    current_answers[payload['question']] = payload['answer']
    session.meta['answers'] = current_answers

    return replies
