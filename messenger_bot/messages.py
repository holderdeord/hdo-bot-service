from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.translation import ugettext as _
import json

from quiz.models import Promise

TYPE_ANSWER = 'ANSWER'
TYPE_NEXT = 'NEXT'
TYPE_SESSION_RESET = 'SESSION_RESET'
TYPE_HELP = 'HELP'
TYPE_GET_STARTED = 'GET_STARTED'


def format_text(recipient_id, text):
    return {
        "recipient": {"id": recipient_id},
        "message": {
            "text": text,
        }
    }


def format_quick_reply_next(recipient_id, text, button_text, session_id):
    quick_reply = {
        "content_type": "text",
        "title": button_text,
        "payload": json.dumps({
            "type": TYPE_NEXT,
            "chat_session": str(session_id)
        })
    }
    return format_quick_replies(recipient_id, [quick_reply], text)


def format_quick_replies(recipient_id, quick_replies, button_text='?'):
    return {
        "recipient": {"id": recipient_id},
        "message": {
            "text": button_text,
            "quick_replies": quick_replies
        }
    }


def format_button(recipient_id, button_text, buttons):
    """ Ref: https://developers.facebook.com/docs/messenger-platform/send-api-reference/button-template """
    return {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": button_text,
                    "buttons": buttons,
                }
            }
        }
    }


def format_question(recipient_id, question, question_text, session_id):
    buttons = [
        {
            "content_type": "text",
            "title": _("fulfilled").capitalize(),
            "payload": json.dumps({
                'question': question['pk'],
                'answer': Promise.FULFILLED,
                'type': TYPE_ANSWER,
                'chat_session': str(session_id)
             }),
            "image_url": static('messenger_bot/icon_fulfilled.png')
        },
        {
            "content_type": "text",
            "title": _('broken').capitalize(),
            "payload": json.dumps({
                'question': question['pk'],
                'answer': Promise.BROKEN,
                'type': TYPE_ANSWER,
                'chat_session': str(session_id)
             }),
            "image_url": static('messenger_bot/icon_broken.png')
        }
    ]

    return format_quick_replies(recipient_id, buttons, question_text)


def format_image_attachment(recipient_id, url):
    return {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": url
                }
            }
        }
    }
