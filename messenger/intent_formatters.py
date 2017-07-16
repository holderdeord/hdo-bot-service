from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.translation import ugettext as _
import json

from messenger.api.formatters import format_quick_replies
from messenger.intents import INTENT_NEXT_ITEM, INTENT_ANSWER_QUIZ_QUESTION
from quiz.models import Promise


def format_quick_reply_next(recipient_id, text, button_text):
    quick_reply = {
        "content_type": "text",
        "title": button_text,
        "payload": json.dumps({
            "intent": INTENT_NEXT_ITEM,
        })
    }
    return format_quick_replies(recipient_id, [quick_reply], text)


def format_question(recipient_id, question, question_text):
    buttons = [
        {
            "content_type": "text",
            "title": _("fulfilled").capitalize(),
            "payload": json.dumps({
                'question': question['pk'],
                'answer': Promise.FULFILLED,
                'intent': INTENT_ANSWER_QUIZ_QUESTION,
             }),
            "image_url": static('messenger/icon_fulfilled.png')
        },
        {
            "content_type": "text",
            "title": _('broken').capitalize(),
            "payload": json.dumps({
                'question': question['pk'],
                'answer': Promise.BROKEN,
                'intent': INTENT_ANSWER_QUIZ_QUESTION,
             }),
            "image_url": static('messenger/icon_broken.png')
        }
    ]

    return format_quick_replies(recipient_id, buttons, question_text)

