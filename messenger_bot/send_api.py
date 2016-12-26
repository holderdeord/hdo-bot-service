import json

import requests
from django.conf import settings
from django.utils.translation import ugettext as _

TYPE_ANSWER = 'ANSWER'


def send_message(data):
    access_token = settings.FACEBOOK_APP_ACCESS_TOKEN
    response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + access_token, json=data)
    return response.json()


def send_text(recipient_id, text):
    data = {
        "recipient": {"id": recipient_id},
        "message": {
            "text": text,
        }
    }
    return send_message(data)


def send_button(recipient_id, button_text, buttons):
    """ Ref: https://developers.facebook.com/docs/messenger-platform/send-api-reference/button-template """
    data = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": button_text,
                    "buttons": buttons
                }
            }
        }
    }
    return send_message(data)


def send_question(recipient_id, question):
    buttons = [
        {
            "type": "postback",
            "title": _("Holdt løftet"),
            "payload": json.dumps({
                'question': question['id'],
                'answer': True,
                'type': TYPE_ANSWER
             })
        },
        {
            "type": "postback",
            "title": _('Brutt løftet'),
            "payload": json.dumps({
                'question': question['id'],
                'answer': False,
                'type': TYPE_ANSWER
             })
        }
    ]

    return send_button(recipient_id, question['text'], buttons)


def get_user_profile(user_id):
    params = {
        'fields': 'first_name',  # ,last_name,profile_pic, locale, timezone,gender',
        'access_token': settings.FACEBOOK_APP_ACCESS_TOKEN
    }
    url = 'https://graph.facebook.com/v2.6/{user_id}/'.format(user_id=user_id)

    response = requests.get(url, params)

    return response.json()
