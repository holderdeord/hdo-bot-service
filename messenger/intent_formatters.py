import json
import logging
import random

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.translation import ugettext as _

from messenger.api.formatters import format_quick_replies, format_text
from messenger.intents import (INTENT_NEXT_ITEM, INTENT_ANSWER_QUIZ_QUESTION, INTENT_GOTO_MANUSCRIPT,
                               INTENT_ANSWER_VG_QUESTION, INTENT_RESET_SESSION, INTENT_GET_STARTED,
                               INTENT_RESET_ANSWERS, INTENT_RESET_ANSWERS_CONFIRM, INTENT_VG_CATEGORY_SELECT,
                               INTENT_SHOW_ANSWERS)
from messenger.utils import get_result_url, get_messenger_bot_url, count_and_sort_answers
from quiz.models import Promise, ManuscriptItem, VoterGuideAlternative, Manuscript
from quiz.utils import PARTY_SHORT_NAMES

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
                    "type": "postback",
                    "title": "Vis mine svar",
                    "payload": json.dumps({'intent': INTENT_SHOW_ANSWERS})
                },
                {
                    "type": "postback",
                    "title": "Velg nytt tema",
                    "payload": json.dumps({
                        'intent': INTENT_GOTO_MANUSCRIPT,
                        'manuscript': Manuscript.objects.get_default(default=Manuscript.DEFAULT_VOTER_GUIDE).pk
                    })
                },
                {
                    "type": "postback",
                    "title": "Start på nytt",
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


def format_vg_categories(recipient_id, manuscripts, text, num_pages, page, max_qrs):
    buttons = []
    alt_text = []
    if page == 1:
        for idx, m in enumerate(manuscripts, start=1):
            alt_text.append('\n{} {}: {}'.format(idx, m.hdo_category.name, m.hdo_category.label))
    alt_text = ''.join(alt_text)

    if num_pages == 1:
        # This is easy. Create unpaged category list
        for idx, m in enumerate(manuscripts, start=1):
            buttons.append({
                "content_type": "text",
                "title": '{} {}'.format(idx, m.hdo_category.label),
                "payload": json.dumps({
                    'manuscript': m.pk,
                    'intent': INTENT_GOTO_MANUSCRIPT
                }),
            })
        return format_quick_replies(recipient_id, buttons, text + alt_text + '\n')

    # More than 1 page, then create a paged category list.
    # The paged list needs a next button with current manuscript order and next page in payload
    start = 1
    if page != 1:
        start = max_qrs * (page - 1) + 1
    for idx, m in enumerate(manuscripts[start-1:], start=start):
        buttons.append({
            "content_type": "text",
            "title": '{} {}'.format(idx, m.hdo_category.label),
            "payload": json.dumps({
                'manuscript': m.pk,
                'intent': INTENT_GOTO_MANUSCRIPT
            }),
        })
        # End of page?
        if idx % max_qrs == 0:
            # Not last page?
            if page != num_pages:
                buttons.append({
                    "content_type": "text",
                    "title": 'Vis resten',
                    "payload": json.dumps({
                        'intent': INTENT_VG_CATEGORY_SELECT,
                        'category_page': page + 1,
                        'manuscript_selection': [m.pk for m in manuscripts]
                    }),
                })
            break
    return format_quick_replies(recipient_id, buttons, text + alt_text + '\n')


def _order_alternatives(alts):
    """ Pop don't know alts, randomize and append "don't know" alt last """
    new_alts = []
    no_answer = []
    for alt in alts:
        if alt['no_answer']:
            no_answer.append(alt)
        else:
            new_alts.append(alt)

    random.shuffle(new_alts)
    return new_alts + no_answer


def format_vg_alternatives(recipient_id, manus, text):
    labels = ['1 👍', '2 😃', '3 👌', '4 ❤', '5 👏', '6 😍', '7 💪', '8 👊']
    buttons = []
    alt_text = ''

    alts = _order_alternatives(manus['voter_guide_alternatives'])
    for i, alt in enumerate(alts):
        buttons.append({
            "content_type": "text",
            "title": labels[i],
            "payload": json.dumps({
                'alternative': alt['pk'],
                'intent': INTENT_ANSWER_VG_QUESTION
            }),
        })
        alt_text += '\n{} {}'.format(labels[i], alt['text'])

    text = '{}{}'.format(text, alt_text)
    return format_quick_replies(recipient_id, buttons, text)


def format_reset_answer(recipient_id):
    quick_replies = [{
            "content_type": "text",
            "title": "Nei, jeg beholder de",
            "payload": json.dumps({
                "intent": INTENT_RESET_SESSION,
            })
        },
        {
            "content_type": "text",
            "title": '💥 Slett alt!',
            "payload": json.dumps({
                "intent": INTENT_RESET_ANSWERS_CONFIRM,
            })
        }
    ]
    return format_quick_replies(recipient_id, quick_replies, "Skal vi slette alle svarene dine?")


def format_vg_result_reply(sender_id, session):
    alts = VoterGuideAlternative.objects.filter(answers__answer_set__session=session)

    grouped_by_counts = count_and_sort_answers(alts)

    text = 'Du er mest enig med:\n'
    place = 1
    medals = {1: '🥇', 2: '🥈', 3: '🥉'}
    for count, parties in grouped_by_counts.items():
        medal = medals.get(place, '')
        if medal:
            medal += ' '

        text += '{}{}\n'.format(medal, ', '.join([PARTY_SHORT_NAMES[p] for p in parties]))
        place += 1

    return format_text(sender_id, text)


def format_result_or_share_buttons(session):
    res_url = get_result_url(session)
    messenger_bot_url = get_messenger_bot_url()
    hdo_share_image = 'https://data.holderdeord.no/assets/og_logo-8b1cb2e26b510ee498ed698c4e9992df.png'
    return [
        {
            "type": "web_url",
            "url": res_url,
            "title": "Vis mine svar i detalj",
        },
        {
            "type": "element_share",
            "share_contents": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": "Jeg tok HDO sin valgomat, prøv du også!",
                                "image_url": hdo_share_image,
                                "default_action": {
                                    "type": "web_url",
                                    "url": messenger_bot_url
                                },
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": messenger_bot_url,
                                        "title": 'Ok, jeg prøver'
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
    ]

