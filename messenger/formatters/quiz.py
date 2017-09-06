import json
import random

from django.contrib.staticfiles.templatetags.staticfiles import static

from messenger import intents
from messenger.api.formatters import format_quick_replies
from quiz.models import Promise
from quiz.utils import PARTY_SHORT_NAMES


def format_quiz_alternatives(recipient_id, manus):
    buttons = []
    alts = manus['quiz_alternatives']
    random.shuffle(alts)

    for alt in alts:
        buttons.append({
            "content_type": "text",
            "title": PARTY_SHORT_NAMES[alt['text']],
            "payload": json.dumps({
                'alternative': alt['pk'],
                'intent': intents.INTENT_ANSWER_QUIZ_QUESTION
            }),
        })

    return format_quick_replies(recipient_id, buttons, manus['name'])


def format_broken_question(recipient_id, question, question_text):
    buttons = [
        {
            "content_type": 'text',
            "title": 'Holdt',
            "payload": json.dumps({
                'question': question['pk'],
                'answer': Promise.FULFILLED,
                'intent': intents.INTENT_ANSWER_QUIZ_BROKEN_QUESTION,
             }),
            "image_url": static('messenger/icon_fulfilled.png')
        },
        {
            "content_type": 'text',
            "title": 'Brutt',
            "payload": json.dumps({
                'question': question['pk'],
                'answer': Promise.BROKEN,
                'intent': intents.INTENT_ANSWER_QUIZ_BROKEN_QUESTION,
             }),
            "image_url": static('messenger/icon_broken.png')
        }
    ]

    return format_quick_replies(recipient_id, buttons, question_text)
