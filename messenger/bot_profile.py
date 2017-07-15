import json
import logging
from django.conf import settings
from django.utils.translation import ugettext as _

from messenger.intents import INTENT_GET_HELP, INTENT_RESET_SESSION, INTENT_GET_STARTED


logger = logging.getLogger(__name__)


def format_profile():
    """ Ref: https://developers.facebook.com/docs/messenger-platform/messenger-profile/persistent-menu """
    return {
        "get_started": {
            "payload": json.dumps({'TYPE': INTENT_GET_STARTED})
        },
        "greeting": [
            {
                "locale": "default",
                "text": _("Hi {{user_first_name}}!")
            }
        ],
        "persistent_menu": [{
            "locale": "default",
            "composer_input_disabled": False,  # Disable/Enable user input
            "call_to_actions": [
                {
                    "type": "postback",
                    "title": _("Get help"),
                    "payload": json.dumps({'intent': INTENT_GET_HELP})
                },
                {
                    "type": "postback",
                    "title": _("Start over"),
                    "payload": json.dumps({'intent': INTENT_RESET_SESSION})
                },
                {
                    "type": "web_url",
                    "title": _("About"),
                    "url": settings.BASE_URL
                }
            ]
        }]
    }
