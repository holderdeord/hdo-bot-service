import json
import logging

from messenger.messages import TYPE_SESSION_RESET, TYPE_HELP, TYPE_GET_STARTED

logger = logging.getLogger(__name__)


def format_profile():
    profile = {}
    profile.update(get_get_started())
    profile.update(get_greeting_text())
    profile.update(get_persistent_menu())
    return profile


def get_persistent_menu():
    """ Ref: https://developers.facebook.com/docs/messenger-platform/messenger-profile/persistent-menu """
    return {
        "persistent_menu": [{
            "locale": "default",
            "composer_input_disabled": False,  # Disable/Enable user input
            "call_to_actions": [
                {
                    "type": "postback",
                    "title": "Hjelp meg litt",
                    "payload": json.dumps({'type': TYPE_HELP})
                },
                {
                    "type": "postback",
                    "title": "Ny quiz (slett sesjon)",
                    "payload": json.dumps({'type': TYPE_SESSION_RESET})
                },
                {
                    "type": "web_url",
                    "title": "Om quizen",
                    "url": "http://hdo-quiz.herokuapp.com/"
                }
            ]
        }]
    }


def get_greeting_text():
    return {
        "greeting": [
            {
                "locale": "default",
                "text": "Hei {{user_first_name}}!"
            }
        ]
    }


def get_get_started():
    return {
        "get_started": {
            "payload": json.dumps({'TYPE': TYPE_GET_STARTED})
        }
    }
