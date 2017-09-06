import json
import logging
import random


from messenger.api.formatters import format_quick_replies, format_text
from messenger import intents
from messenger.utils import get_quiz_answer_set_url, count_and_sort_answers
from quiz.models import VoterGuideAlternative
from quiz.utils import PARTY_SHORT_NAMES

logger = logging.getLogger(__name__)


def format_categories(recipient_id, manuscripts, text, num_pages, page, max_qrs, quiz):
    # FIXME: Move to formatters/general.py
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
                    'intent': intents.INTENT_GOTO_MANUSCRIPT
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
                'intent': intents.INTENT_GOTO_MANUSCRIPT
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
                        'intent': intents.INTENT_CATEGORY_SELECT,
                        'category_page': page + 1,
                        'manuscript_selection': [m.pk for m in manuscripts],
                        'quiz': quiz,
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
                'intent': intents.INTENT_ANSWER_VG_QUESTION
            }),
        })
        alt_text += '\n{} {}'.format(labels[i], alt['text'])

    text = '{}{}'.format(text, alt_text)
    return format_quick_replies(recipient_id, buttons, text)


def format_vg_result_reply(sender_id, session):
    alts = VoterGuideAlternative.objects.filter(answers__answer_set__session=session)

    grouped_by_counts = count_and_sort_answers(alts)
    total_count = alts.count()

    text = 'Du er mest enig med:\n'
    medals = {1: '🥇', 2: '🥈', 3: '🥉'}
    for i, item in enumerate(grouped_by_counts.items(), start=1):
        count, parties = item
        rank = medals.get(i, '{}.'.format(i))

        parties_formatted = ', '.join([PARTY_SHORT_NAMES[p] for p in parties])
        text += '{} {} {}\n'.format(rank, parties_formatted, '{:.1f}%'.format((count / total_count) * 100))

    return format_text(sender_id, text)


def format_vg_result_button(session):
    res_url = get_quiz_answer_set_url(session)
    return [
        {
            "type": "web_url",
            "url": '{}?shared=1'.format(res_url),
            "title": "Vis mine svar",
        },
    ]
