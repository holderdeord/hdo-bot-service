import logging

from messenger.api.formatters import format_text
from messenger.intent_formatters import (format_vg_categories, format_vg_alternatives, format_quick_reply_with_intent,
                                         format_vg_show_results_or_next, format_vg_result_reply)
from messenger.intents import INTENT_NEXT_QUESTION
from messenger.utils import get_voter_guide_manuscripts, get_next_vg_manuscript
from quiz.models import VoterGuideAlternative, Manuscript

logger = logging.getLogger(__name__)


def get_voter_guide_category_replies(sender_id, session, payload, text):
    """ Show manuscripts of type voter guide as quick replies """
    manuscripts = get_voter_guide_manuscripts(session)

    if not manuscripts:
        return [format_text(sender_id, 'Wow! 😮 Du har fullført alle kategoriene 🤓🤓 Imponerende 😎'),
                format_text(sender_id, 'TODO: lenke til resultatsiden, call to action eller deling her?')]

    return [format_vg_categories(sender_id, manuscripts, text)]


def get_voter_guide_questions(sender_id, session, payload, text):
    return [format_vg_alternatives(sender_id, session.meta['manuscript'], text)]


def get_vg_question_replies(sender_id, session, payload):
    alt = VoterGuideAlternative.objects.get(pk=payload['alternative'])
    next_text = "Du svarte \'{}\'".format(alt.text)

    next_manuscript = get_next_vg_manuscript(session)
    if next_manuscript:
        extra_payload = {'manuscript': next_manuscript.pk if next_manuscript else None}
        return [format_quick_reply_with_intent(
            sender_id, "Neste spørsmål", next_text, INTENT_NEXT_QUESTION, extra_payload)]

    # Emptied out the category, link to root
    extra_payload = {'manuscript': Manuscript.objects.get_default().pk}
    finished_msg = 'Du har nå gått gjennom alle spørsmålene vi har for denne kategorien.'
    more_cats_msg = 'Velg en ny kategori og besvare spørsmålene for å gjøre resultatene dine mer presis.'

    return [
        format_text(sender_id, next_text),
        format_text(sender_id, finished_msg),
        format_vg_result_reply(sender_id, session),
        format_quick_reply_with_intent(
            sender_id, 'Flere kategorier!', more_cats_msg, INTENT_NEXT_QUESTION, extra_payload)]


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
    extra_payload = {'manuscript': Manuscript.objects.get_default().pk}
    finished_msg = 'Du har nå gått gjennom alle spørsmålene vi har for denne kategorien.'
    more_cats_msg = 'Velg en ny kategori og besvare spørsmålene for å gjøre resultatene dine mer presis.'

    return [
        format_text(sender_id, finished_msg),
        format_vg_result_reply(sender_id, session),
        format_quick_reply_with_intent(
            sender_id, 'Flere kategorier!', more_cats_msg, INTENT_NEXT_QUESTION, extra_payload)]
