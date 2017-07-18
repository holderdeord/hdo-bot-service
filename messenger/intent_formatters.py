import json
import logging

from typing import Iterable
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.translation import ugettext as _

from messenger.api.formatters import format_quick_replies
from messenger.intents import (INTENT_NEXT_ITEM, INTENT_ANSWER_QUIZ_QUESTION, INTENT_GOTO_MANUSCRIPT,
                               INTENT_ANSWER_VG_QUESTION, INTENT_GET_HELP, INTENT_RESET_SESSION, INTENT_GET_STARTED)
from quiz.models import Promise, Manuscript, ManuscriptItem

logger = logging.getLogger(__name__)


def format_bot_profile():
    """ Ref: https://developers.facebook.com/docs/messenger-platform/messenger-profile/persistent-menu """
    return {
        "get_started": {
            "payload": json.dumps({'intent': INTENT_GET_STARTED})
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


def format_quick_reply_next(recipient_id, button_text, text):
    quick_reply = {
        "content_type": "text",
        "title": button_text,
        "payload": json.dumps({
            "intent": INTENT_NEXT_ITEM,
        })
    }
    return format_quick_replies(recipient_id, [quick_reply], text)


def format_quick_reply_with_intents(recipient_id, item):
    quick_replies = []
    for text, action in ManuscriptItem.QUICK_REPLY_FIELDS.items():
        if item.get(text):
            manuscript_id = item.get(action)
            quick_replies += [{
                "content_type": "text",
                "title": item.get(text),
                "payload": json.dumps({
                    "intent": INTENT_GOTO_MANUSCRIPT if manuscript_id else INTENT_NEXT_ITEM,
                    "manuscript": manuscript_id
                })
            }]
    return format_quick_replies(recipient_id, quick_replies, item['text'])


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


def format_vg_categories(recipient_id, manuscripts: Iterable[Manuscript], text):
    buttons = []
    alt_text = ''
    for idx, m in enumerate(manuscripts, start=1):
        buttons.append({
            "content_type": "text",
            "title": '{} {}'.format(idx, m.hdo_category.label),
            "payload": json.dumps({
                'manuscript': m.pk,
                'intent': INTENT_GOTO_MANUSCRIPT
            }),
        })
        alt_text += '\n{} {}: {}'.format(idx, m.hdo_category.name, m.hdo_category.label)
    return format_quick_replies(recipient_id, buttons, text + alt_text + '\n')


def format_vg_alternatives(recipient_id, name, alternatives, text):
    labels = ['1 💜', '2 💙', '3 💚', '4 💛', '5 ❤', '6 ♦']
    buttons = []
    alt_text = ''
    for i, alt in enumerate(alternatives):
        buttons.append({
            "content_type": "text",
            "title": labels[i],
            "payload": json.dumps({
                'alternative': alt['pk'],
                'intent': INTENT_ANSWER_VG_QUESTION
            }),
        })
        alt_text += '\n{} {}'.format(labels[i], alt['text'])

    text = 'Temaet er {}\n\n{}{}'.format(name, text, alt_text)
    return format_quick_replies(recipient_id, buttons, text)
