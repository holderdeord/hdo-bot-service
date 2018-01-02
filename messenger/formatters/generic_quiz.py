import json
import random

from django.contrib.staticfiles.templatetags.staticfiles import static

from messenger import intents
from messenger.api.formatters import format_quick_replies
from quiz.templatetags.quiz_extras import get_party_image_url


def _get_image_url(alt):
    alt_text = alt['text'].lower()
    boolean_alts = {
        'ja': static('messenger/icon_thumb_up.png'),
        'nei': static('messenger/icon_thumb_down.png')
    }
    for b in boolean_alts.keys():
        if alt_text.startswith(b):
            return boolean_alts[b]

    party_image = get_party_image_url(alt['text'], image_dir='images_white')
    if party_image != '':
        return party_image


def _should_shuffle(alts):
    sorted_alts = sorted(alts, key=lambda a: a['text'])
    if set(map(lambda x: x['text'].lower(), sorted_alts)) == {'ja', 'nei'}:
        return False

    return True


def format_quiz_question(recipient_id, manus):
    buttons = []
    alts = manus['quiz_alternatives']

    if _should_shuffle(alts):
        random.shuffle(alts)
    else:
        alts = sorted(alts, key=lambda a: a['text'])

    for alt in alts:
        btn = {
            "content_type": "text",
            "title": alt['text'],
            "payload": json.dumps({
                'alternative': alt['pk'],
                'intent': intents.INTENT_ANSWER_GENERIC_QUIZ_QUESTION
            }),
        }
        img = _get_image_url(alt)
        if img is not None:
            btn['image_url'] = img

        buttons.append(btn)

    return format_quick_replies(recipient_id, buttons, manus['name'])


def format_yes_or_no_question(recipient_id, manus):
    alts = manus['quiz_alternatives']
    alts = sorted(alts, key=lambda a: a['text'])  # ninja sort (Ja er før Nei)
    buttons = [
        {
            "content_type": 'text',
            "title": alts[0]['text'],
            "payload": json.dumps({
                'alternative': alts[0]['pk'],
                'intent': intents.INTENT_ANSWER_GENERIC_QUIZ_QUESTION,
             }),
            "image_url": static('messenger/icon_thumb_up.png')
        },
        {
            "content_type": 'text',
            "title": alts[1]['text'],
            "payload": json.dumps({
                'alternative': alts[1]['pk'],
                'intent': intents.INTENT_ANSWER_GENERIC_QUIZ_QUESTION,
             }),
            "image_url": static('messenger/icon_thumb_down.png')
        }
    ]

    return format_quick_replies(recipient_id, buttons, manus['name'])
