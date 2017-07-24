import logging

from collections import defaultdict, OrderedDict

from messenger.api.formatters import format_text
from messenger.intent_formatters import format_vg_categories, format_vg_alternatives, format_quick_reply_next
from messenger.utils import get_voter_guide_manuscripts
from quiz.models import VoterGuideAlternative


logger = logging.getLogger(__name__)


def get_voter_guide_category_replies(sender_id, session, payload, text):
    """ Show manuscripts of type voter guide as quick replies """
    manuscripts = get_voter_guide_manuscripts(session)
    return [format_vg_categories(sender_id, manuscripts, text)]


def get_voter_guide_questions(sender_id, session, payload, text):
    manus = session.meta['manuscript']

    return [format_vg_alternatives(sender_id, manus['name'], manus['voter_guide_alternatives'], text)]


def get_vg_question_replies(sender_id, session, payload):
    alt = VoterGuideAlternative.objects.get(pk=payload['alternative'])
    return [format_text(sender_id, "Du svarte \'{}\'".format(alt.text))]


def get_voter_guide_result(sender_id, session, payload):
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

    return [format_quick_reply_next(sender_id, "Videre", text)]
