import json
import logging
from collections import defaultdict, OrderedDict

from typing import Iterable
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.translation import ugettext as _

from messenger.api.formatters import format_quick_replies, format_text
from messenger.intents import (INTENT_NEXT_ITEM, INTENT_ANSWER_QUIZ_QUESTION, INTENT_GOTO_MANUSCRIPT,
                               INTENT_ANSWER_VG_QUESTION, INTENT_GET_HELP, INTENT_RESET_SESSION, INTENT_GET_STARTED,
                               INTENT_RESET_ANSWERS, INTENT_RESET_ANSWERS_CONFIRM)
from quiz.models import Promise, Manuscript, ManuscriptItem, HdoCategory, VoterGuideAlternative

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
            "composer_input_disabled": True,  # Disable/Enable user input
            "call_to_actions": [
                {
                    "type": "nested",
                    "title": _("Get help"),
                    "call_to_actions": [
                        {
                            "type": "postback",
                            "title": _("Get help"),
                            "payload": json.dumps({'intent': INTENT_GET_HELP})
                        },
                        {
                            "type": "web_url",
                            "title": _("About"),
                            "url": settings.BASE_URL
                        }
                    ]
                },
                {
                    "type": "postback",
                    "title": _("Start over"),
                    "payload": json.dumps({'intent': INTENT_RESET_SESSION})
                },
                {
                    "type": "postback",
                    "title": _("Reset my answers"),
                    "payload": json.dumps({'intent': INTENT_RESET_ANSWERS})
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
    return format_quick_reply_with_intent(recipient_id, button_text, text, INTENT_NEXT_ITEM)


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


def format_vg_alternatives(recipient_id, manus, text):
    labels = ['1 👍', '2 😃', '3 👌', '4 ❤', '5 👏', '6 😍', '7 💪', '8 👊']
    buttons = []
    alt_text = ''
    for i, alt in enumerate(manus['voter_guide_alternatives']):
        buttons.append({
            "content_type": "text",
            "title": labels[i],
            "payload": json.dumps({
                'alternative': alt['pk'],
                'intent': INTENT_ANSWER_VG_QUESTION
            }),
        })
        alt_text += '\n{} {}'.format(labels[i], alt['text'])

    cat = HdoCategory.objects.get(pk=manus['hdo_category'])  # FIXME: Put name in serializer
    text = '{} - {}\n{}{}'.format(cat.name, manus['name'], text, alt_text)
    return format_quick_replies(recipient_id, buttons, text)


def format_reset_answer(recipient_id):
    quick_replies = [{
            "content_type": "text",
            "title": "Nei, bare fortsett",
            "payload": json.dumps({
                "intent": INTENT_NEXT_ITEM,
            })
        },
        {
            "content_type": "text",
            "title": 'Slett alt!',
            "payload": json.dumps({
                "intent": INTENT_RESET_ANSWERS_CONFIRM,
            })
        }
    ]
    return format_quick_replies(recipient_id, quick_replies, "Skal vi slette alle svarene dine?")


def format_vg_show_results_or_next(recipient_id, next_manuscript, text):
    quick_replies = [{
            "content_type": "text",
            "title": "Foreløbig resultat",
            "payload": json.dumps({
                "intent": INTENT_NEXT_ITEM,
            })
        },
        {
            "content_type": "text",
            "title": 'Neste spørsmål',
            "payload": json.dumps({
                "intent": INTENT_GOTO_MANUSCRIPT,
                "manuscript": next_manuscript
            })
        }
    ]
    return format_quick_replies(recipient_id, quick_replies, text)


def format_vg_result_reply(sender_id, session):
    alts = VoterGuideAlternative.objects.filter(answers__answer_set__session=session)

    # FIXME: Use parties instead of promisor_name (after re-import), promisor can be a government (ie multiple parties)
    # Note: Each alternative can have more than 1 promise tied to the same party
    parties_by_alternative = defaultdict(set)
    for alt in alts.all():
        for p in alt.promises.all():
            parties_by_alternative[alt.pk].add(p.promisor_name)

    # Count and sort number of answers by party
    total_count = alts.count()
    counts = defaultdict(lambda: 0)
    for alt, parties in parties_by_alternative.items():
        for p in parties:
            counts[p] += 1
    ordered_counts = OrderedDict(sorted(counts.items(), key=lambda c: c[1], reverse=True))

    text = 'Disse partiene er du mest enig i:\n\n'
    place = 1
    medals = {1: '🥇', 2: '🥈', 3: '🥉'}
    for party, count in ordered_counts.items():
        medal = medals.get(place, '')
        if medal:
            medal += ' '
        text += '{}{}: {:.1f}%\n'.format(medal, party, (count/total_count)*100)
        place += 1

    return format_text(sender_id, text)
