import json
import random

from messenger import intents
from messenger.api.formatters import format_quick_replies


def format_quiz_alternatives(recipient_id, manus):
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
