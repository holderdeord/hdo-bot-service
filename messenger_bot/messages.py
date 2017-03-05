import json

from django.utils.translation import ugettext as _

from quiz.models import Promise

TYPE_ANSWER = 'ANSWER'
TYPE_NEXT = 'NEXT'


def format_text(recipient_id, text):
    return {
        "recipient": {"id": recipient_id},
        "message": {
            "text": text,
        }
    }


def format_quick_reply_next(recipient_id, text, session_id):
    quick_reply = {
        "content_type": "text",
        "title": text,
        "payload": json.dumps({
            "type": TYPE_NEXT,
            "chat_session": str(session_id)
        })
    }
    return format_quick_replies(recipient_id, [quick_reply])


def format_quick_replies(recipient_id, quick_replies, text='?'):
    return {
        "recipient": {"id": recipient_id},
        "message": {
            "text": text,
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


def format_question(recipient_id, question, session_id):
    buttons = [
        {
            "type": "postback",
            "title": _("Holdt løftet"),
            "payload": json.dumps({
                'question': question['pk'],
                'answer': Promise.FULFILLED,
                'type': TYPE_ANSWER,
                'chat_session': str(session_id)
             })
        },
        {
            "type": "postback",
            "title": _('Brutt løftet'),
            "payload": json.dumps({
                'question': question['pk'],
                'answer': Promise.BROKEN,
                'type': TYPE_ANSWER,
                'chat_session': str(session_id)
             })
        }
    ]

    return format_button(recipient_id, question['body'], buttons)


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
