import logging

import math

from messenger.api.formatters import format_text
from messenger.intent_formatters import (format_vg_categories, format_vg_alternatives, format_quick_reply_with_intent,
                                         format_vg_show_results_or_next, format_vg_result_reply)
from messenger.intents import INTENT_NEXT_QUESTION
from messenger.utils import get_voter_guide_manuscripts, get_next_vg_manuscript
from quiz.models import VoterGuideAlternative, Manuscript

logger = logging.getLogger(__name__)

MAX_QUICK_REPLIES = 7


def get_voter_guide_category_replies(sender_id, session, payload, text):
    """ Show manuscripts of type voter guide as quick replies """
    selection = None
    if payload:
        selection = payload.get('manuscript_selection')
    manuscripts = get_voter_guide_manuscripts(session, selection)

    if not manuscripts:
        return [format_text(sender_id, 'Wow! 😮 Du har gått gjennom alle temaene 🤓🤓 Imponerende 😎'),
                format_text(sender_id, 'TODO: lenke til resultatsiden, call to action eller deling her?')]

    num_pages = int(math.ceil(len(manuscripts) / MAX_QUICK_REPLIES))
    page = payload.get('category_page', 1) if payload else 1

    return [format_vg_categories(sender_id, manuscripts, text, num_pages, page, MAX_QUICK_REPLIES)]


def get_voter_guide_questions(sender_id, session, payload, text):
    return [format_vg_alternatives(sender_id, session.meta['manuscript'], text)]


def _get_alternative_affiliations(alt: VoterGuideAlternative):
    affils = list(set(alt.promises.values_list('promisor_name', flat=True)))

    # Format
    if len(affils) == 1:
        return affils[0]

    if len(affils) > 1:
        start = ', '.join(affils[:-1])
        return '{} og {}'.format(start, affils[-1])

    return ''


def get_vg_question_replies(sender_id, session, payload):
    alt = VoterGuideAlternative.objects.get(pk=payload['alternative'])
    next_text = 'Du mener det samme som {}'.format(_get_alternative_affiliations(alt))

    next_manuscript = get_next_vg_manuscript(session)
    if next_manuscript:
        # TODO: If "vet ikke", then reply x
        session.meta['next_manuscript'] = next_manuscript.pk if next_manuscript else None
        return [format_text(sender_id, next_text)]

    # Emptied out the category, link to root
    extra_payload = {'manuscript': Manuscript.objects.get_default(default=Manuscript.DEFAULT_VOTER_GUIDE).pk}
    finished_msg = 'Du har nå gått gjennom alle spørsmålene med dette temaet.'
    more_cats_msg = 'Velg nytt tema for å gjøre ditt resultat mer presist.'

    return [
        format_text(sender_id, next_text),
        format_text(sender_id, finished_msg),
        format_vg_result_reply(sender_id, session),
        format_quick_reply_with_intent(
            sender_id, 'Neste tema!', more_cats_msg, INTENT_NEXT_QUESTION, extra_payload)]


def get_next_vg_question_reply(sender_id, session, payload):
    # Link to an unanswered and not skipped manuscript in the same category
    next_text = "Når du er klar kan du gå videre til neste spørsmål"
    next_manuscript = get_next_vg_manuscript(session)
    extra_payload = {'manuscript': next_manuscript.pk if next_manuscript else None}
    return format_quick_reply_with_intent(sender_id, "Neste spørsmål", next_text, INTENT_NEXT_QUESTION, extra_payload)


def get_voter_guide_result(sender_id, session, payload):
    return [format_vg_result_reply(sender_id, session), get_next_vg_question_reply(sender_id, session, payload)]


def get_show_res_or_next(sender_id, session, payload):
    next_manuscript = get_next_vg_manuscript(session)
    if next_manuscript:
        text = "Vil du se foreløpig resultat, eller vil du gå videre til neste spørsmål?"
        # More questions in category, yey!
        return [format_vg_show_results_or_next(sender_id, next_manuscript.pk, text)]

    # Emptied out the category, link to root
    extra_payload = {'manuscript': Manuscript.objects.get_default(default=Manuscript.DEFAULT_VOTER_GUIDE).pk}
    finished_msg = 'Du har nå gått gjennom alle spørsmålene med dette temaet.'
    more_cats_msg = 'Velg nytt tema for å gjøre ditt resultat mer presist.'

    return [
        format_text(sender_id, finished_msg),
        format_vg_result_reply(sender_id, session),
        format_quick_reply_with_intent(
            sender_id, 'Neste tema!', more_cats_msg, INTENT_NEXT_QUESTION, extra_payload)]
