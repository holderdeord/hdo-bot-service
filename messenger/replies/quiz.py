import json
import random

from django.utils.translation import ugettext as _

from messenger import intents
from messenger.api import get_user_profile
from messenger.api.formatters import format_text, format_image_attachment, format_quick_replies
from messenger.utils import save_answers

# TODO: Add two other quiz types
from quiz.models import Manuscript


def get_quiz_question_replies(sender_id, session, payload=None):
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


def get_quiz_level_replies(sender_id, session, payload, text):
    """ Show available levels as quick replies """
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
