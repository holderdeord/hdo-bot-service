import logging

from collections import defaultdict, OrderedDict

from messenger.api.formatters import format_text
from messenger.intent_formatters import format_vg_categories, format_vg_alternatives, format_quick_reply_next
from messenger.models import ChatSession
from quiz.models import Manuscript, VoterGuideAlternative, VoterGuideAnswer, AnswerSet, HdoCategory

MAX_QUICK_REPLIES = 7

logger = logging.getLogger(__name__)


def _get_voter_guide_manuscripts(session: ChatSession):
    # Voter guide manuscripts
    manuscripts = Manuscript.objects.filter(type=Manuscript.TYPE_VOTER_GUIDE)

    # Already answered
    answers = VoterGuideAnswer.objects.filter(answer_set__session=session)
    # TODO: YOU ARE HERE
    # TODO: tes this
    # TODO: When formatting the INTENT_ANSWER_VG_QUESTION intent, then link to an unanswered manuscript in the same category instead of following the pointer
    answered_ms = manuscripts.filter(voter_guide_alternatives__answers__in=answers).values_list('pk', flat=True)

    # Categories
    exclude_cat = set()
    for c in HdoCategory.objects.all().select_related('manuscripts'):
        ms = c.manuscripts.values_list('pk', flat=True)
        if all([m in answered_ms for m in ms]):
            # All manuscripts answered, exclude cat
            exclude_cat.add(c)

    # Remove categories already answered
    manuscripts = manuscripts.exclude(hdo_category__in=exclude_cat)
    manuscripts = manuscripts.order_by('?').select_related('hdo_category')[:MAX_QUICK_REPLIES]
    return manuscripts


def get_voter_guide_category_replies(sender_id, session, payload, text):
    """ Show manuscripts of type voter guide as quick replies """
    # FIXME: Support paging of quick replies, for now just use random first 7
    manuscripts = _get_voter_guide_manuscripts(session)
    return [format_vg_categories(sender_id, manuscripts, text)]


def get_voter_guide_questions(sender_id, session, payload, text):
    manus = session.meta['manuscript']

    return [format_vg_alternatives(sender_id, manus['name'], manus['voter_guide_alternatives'], text)]


def get_vg_question_replies(sender_id, session, payload):
    # Save answer
    alt = VoterGuideAlternative.objects.get(pk=payload['alternative'])
    answer_set, _ = AnswerSet.objects.get_or_create(session=session)  # reuse answerset
    answer, _ = VoterGuideAnswer.objects.get_or_create(answer_set=answer_set, voter_guide_alternative=alt)

    return [format_text(sender_id, "Du svarte \'{}\'".format(alt.text))]


def get_voter_guide_result(sender_id, session, payload):
    alts = VoterGuideAlternative.objects.filter(answers__answer_set__session=session)

    # FIXME: Use parties instead of promisor_name (after re-import), promisor can be a government (multiple parties)
    # Note: Each alternative can have more than 1 promises tied to the same party
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
