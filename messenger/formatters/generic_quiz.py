import json
import random

from django.contrib.staticfiles.templatetags.staticfiles import static

from messenger import intents
from messenger.api.formatters import format_quick_replies


def format_quiz_question(recipient_id, manus):
    buttons = []
    alts = manus['quiz_alternatives']
    random.shuffle(alts)

    for alt in alts:
        buttons.append({
            "content_type": "text",
            "title": alt['text'],
            "payload": json.dumps({
                'alternative': alt['pk'],
                'intent': intents.INTENT_ANSWER_GENERIC_QUIZ_QUESTION
            }),
        })

    return format_quick_replies(recipient_id, buttons, manus['name'])


def format_yes_or_no_question(recipient_id, manus):
    alts = manus['quiz_alternatives']
    alts = sorted(alts, key=lambda a: a['text'])  # ninja sort (Ja er før Nei)
    buttons = [
        {
            "content_type": 'text',
            "title": alts[0]['text'],
            "payload": json.dumps({
                'alternative': alts[0]['pk'],
                'intent': intents.INTENT_ANSWER_GENERIC_QUIZ_QUESTION,
             }),
            "image_url": static('messenger/icon_thumb_up.png')
        },
        {
            "content_type": 'text',
            "title": alts[1]['text'],
            "payload": json.dumps({
                'alternative': alts[1]['pk'],
                'intent': intents.INTENT_ANSWER_GENERIC_QUIZ_QUESTION,
             }),
            "image_url": static('messenger/icon_thumb_down.png')
        }
    ]

    return format_quick_replies(recipient_id, buttons, manus['name'])
