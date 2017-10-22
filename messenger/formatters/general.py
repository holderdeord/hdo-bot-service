import json

from messenger import intents
from messenger.api.formatters import format_quick_replies
from quiz.models import Manuscript, ManuscriptItem


def format_bot_profile():
    """ Ref: https://developers.facebook.com/docs/messenger-platform/messenger-profile/persistent-menu """
    return {
        "get_started": {
            "payload": json.dumps({'intent': intents.INTENT_GET_STARTED})
        },
        "greeting": [
            {
                "locale": "default",
                # FIXME: Not static
                "text": 'Hvor godt kjenner du norsk politikk? Før du begynner bør du lese vår personvernpolicy på snakk.holderdeord.no/personvern'
            }
        ],
        "persistent_menu": [{
            "locale": "default",
            "composer_input_disabled": True,  # Disable/Enable user input
            "call_to_actions": [
                {
                    "type": "postback",
                    "title": "Vis mine svar",
                    "payload": json.dumps({'intent': intents.INTENT_SHOW_ANSWERS})
                },
                {
                    "type": "postback",
                    "title": "Velg nytt tema",
                    "payload": json.dumps({
                        'intent': intents.INTENT_GOTO_MANUSCRIPT,
                        'manuscript': Manuscript.objects.get_default(default=Manuscript.DEFAULT_QUIZ).pk
                    })
                },
                {
                    "type": "postback",
                    "title": "Start på nytt",
                    "payload": json.dumps({'intent': intents.INTENT_RESET_ANSWERS})
                },
            ]
        }]
    }


def format_quick_reply_with_intent(recipient_id, button_text, text, intent, extra_payload=None):
    payload = {"intent": intent}

    if extra_payload:
        payload.update(extra_payload)

    quick_reply = {
        "content_type": "text",
        "title": button_text,
        "payload": json.dumps(payload)
    }

    return format_quick_replies(recipient_id, [quick_reply], text)


def format_quick_reply_next(recipient_id, button_text, text):
    return format_quick_reply_with_intent(recipient_id, button_text, text, intents.INTENT_NEXT_ITEM)


def format_quick_replies_with_intent(recipient_id, item):
    """ Look in each QUICK_REPLY_FIELDS and link to manuscripts or next item """
    quick_replies = []
    for text, action in ManuscriptItem.QUICK_REPLY_FIELDS.items():
        if not item.get(text):
            continue

        manuscript_id = item.get(action)
        quick_replies += [{
            "content_type": "text",
            "title": item.get(text),
            "payload": json.dumps({
                "intent": intents.INTENT_GOTO_MANUSCRIPT if manuscript_id else intents.INTENT_NEXT_ITEM,
                "manuscript": manuscript_id
            })
        }]

    return format_quick_replies(recipient_id, quick_replies, item['text'])


def format_reset_answer(recipient_id):
    quick_replies = [{
            "content_type": "text",
            "title": "Nei, jeg beholder de",
            "payload": json.dumps({
                "intent": intents.INTENT_RESET_SESSION,
            })
        },
        {
            "content_type": "text",
            "title": '💥 Slett alt!',
            "payload": json.dumps({
                "intent": intents.INTENT_RESET_ANSWERS_CONFIRM,
            })
        }
    ]
    return format_quick_replies(recipient_id, quick_replies, "Skal vi slette alle svarene dine?")
