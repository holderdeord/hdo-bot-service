import logging

from collections import defaultdict, OrderedDict

from messenger.api.formatters import format_text
from messenger.intent_formatters import format_vg_categories, format_vg_alternatives, format_quick_reply_with_intent
from messenger.intents import INTENT_NEXT_QUESTION
from messenger.utils import get_voter_guide_manuscripts, get_next_vg_manuscript
from quiz.models import VoterGuideAlternative


logger = logging.getLogger(__name__)


def get_voter_guide_category_replies(sender_id, session, payload, text):
    """ Show manuscripts of type voter guide as quick replies """
    manuscripts = get_voter_guide_manuscripts(session)
    return [format_vg_categories(sender_id, manuscripts, text)]


def get_voter_guide_questions(sender_id, session, payload, text):
    manus = session.meta['manuscript']

    return [format_vg_alternatives(sender_id, manus, text)]


def get_vg_question_replies(sender_id, session, payload):
    alt = VoterGuideAlternative.objects.get(pk=payload['alternative'])
    return [format_text(sender_id, "Du svarte \'{}\'".format(alt.text))]


def get_vg_result_reply(sender_id, session):
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


def get_next_vg_question_reply(sender_id, session, payload):
    # Link to an unanswered and not skipped manuscript in the same category
    next_text = "Når du er klar kan du gå videre til neste spørsmål"
    next_manuscript = get_next_vg_manuscript(session, payload)
    extra_payload = {'manuscript': next_manuscript.pk if next_manuscript else None}
    return format_quick_reply_with_intent(sender_id, "Neste spørsmål", next_text, INTENT_NEXT_QUESTION, extra_payload)


def get_voter_guide_result(sender_id, session, payload):
    return [get_vg_result_reply(sender_id, session), get_next_vg_question_reply(sender_id, session, payload)]

