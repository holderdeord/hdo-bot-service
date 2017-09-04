import json

from django.contrib.staticfiles.templatetags.staticfiles import static

from messenger import intents
from messenger.api.formatters import format_quick_replies
from quiz.models import Promise


def format_question(recipient_id, question, question_text):
    buttons = [
        {
            "content_type": 'text',
            "title": 'Holdt',
            "payload": json.dumps({
                'question': question['pk'],
                'answer': Promise.FULFILLED,
                'intent': intents.INTENT_ANSWER_QUIZ_QUESTION,
             }),
            "image_url": static('messenger/icon_fulfilled.png')
        },
        {
            "content_type": 'text',
            "title": 'Brutt',
            "payload": json.dumps({
                'question': question['pk'],
                'answer': Promise.BROKEN,
                'intent': intents.INTENT_ANSWER_QUIZ_QUESTION,
             }),
            "image_url": static('messenger/icon_broken.png')
        }
    ]

    return format_quick_replies(recipient_id, buttons, question_text)
