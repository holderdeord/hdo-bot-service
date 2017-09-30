import logging

import math

from messenger import intents
from messenger.api.formatters import format_text, format_generic_simple
from messenger.formatters.general import format_quick_reply_with_intent
from messenger.formatters.party_quiz import format_quiz_result_reply
from messenger.formatters.voter_guide import (format_quiz_result_button, format_categories, format_vg_alternatives,
                                              format_vg_result_reply)
from messenger.utils import get_manuscripts_for_category_selection, get_next_manuscript
from quiz.models import VoterGuideAlternative, Manuscript, VoterGuideAnswer
from quiz.utils import PARTY_SHORT_NAMES

logger = logging.getLogger(__name__)

MAX_QUICK_REPLIES = 7


def get_category_replies(sender_id, session, payload, text, quiz=False):
    # FIXME: Move to general.py
    """ Show manuscripts of type voter guide or quiz as quick replies """
    selection = None
    level = None
    if payload:
        selection = payload.get('manuscript_selection')
        level = payload.get('level')
        if not quiz:
            quiz = payload.get('quiz', False)

    manuscripts = get_manuscripts_for_category_selection(session, selection, quiz, level)

    if not manuscripts:
        if not hasattr(session, 'answers'):
            return [format_text(sender_id, 'No manuscripts, but no answers?!')]

        image_url = 'https://data.holderdeord.no/assets/og_logo-8b1cb2e26b510ee498ed698c4e9992df.png'
        return [format_generic_simple(
            sender_id,
            'Wow! 😮 Du har svart på alle spørsmålene 🤓🤓 Imponerende 😎',
            format_quiz_result_button(session), image_url=image_url)]

    num_pages = int(math.ceil(len(manuscripts) / MAX_QUICK_REPLIES))
    page = payload.get('category_page', 1) if payload else 1

    return [format_categories(sender_id, manuscripts, text, num_pages, page, MAX_QUICK_REPLIES, quiz)]


def get_vg_questions(sender_id, session, payload, text):
    return [format_vg_alternatives(sender_id, session.meta['manuscript'], text)]


def _get_alternative_affiliation_text(alt: VoterGuideAlternative):
    affils = sorted([PARTY_SHORT_NAMES[party] for party in list(set(alt.promises.values_list('promisor_name', flat=True)))])

    if alt.no_answer:
        # Find parties
        parties_known = list(set(alt.manuscript.voter_guide_alternatives.values_list('promises__promisor_name', flat=True)))
        affils = sorted([PARTY_SHORT_NAMES[x] for x in PARTY_SHORT_NAMES.keys() if x not in set(parties_known)])

    # Format
    if len(affils) == 1:
        if alt.no_answer:
            return '{} har heller ikke et standpunkt i saken'.format(affils[0])

        return 'Du mener det samme som {}'.format(affils[0])

    if len(affils) > 1:
        start = ', '.join(affils[:-1])
        if alt.no_answer:
            return '{} og {} har heller ikke et standpunkt i saken'.format(start, affils[-1])

        return 'Du mener det samme som {} og {}'.format(start, affils[-1])

    return 'Alle partiene mente noe om dette'


def get_vg_question_replies(sender_id, session, payload):
    try:
        alt = VoterGuideAlternative.objects.get(pk=payload['alternative'])
    except VoterGuideAlternative.DoesNotExist:
        return []

    next_text = _get_alternative_affiliation_text(alt)

    next_manuscript = get_next_manuscript(session)
    if next_manuscript:
        session.meta['next_manuscript'] = next_manuscript.pk if next_manuscript else None
        return [format_text(sender_id, next_text)]

    # Emptied out the category, link manuscript select
    extra_payload = {'manuscript': Manuscript.objects.get_default(default=Manuscript.DEFAULT_VOTER_GUIDE).pk}
    num_answers = VoterGuideAnswer.objects.filter(answer_set__session=session).count()
    replies = []

    if 4 <= num_answers < 8:
        # Intro to bot
        finished_msg = 'Du har nå gått gjennom alle spørsmålene med dette temaet.'
        about_bot_text = 'Spørsmålene du får er hentet fra vår løftebase som inneholder alle partiprogrammene.'
        replies += [
            format_text(sender_id, next_text), format_text(sender_id, finished_msg),
            format_quick_reply_with_intent(
                sender_id, 'Neste tema!', about_bot_text, intents.INTENT_NEXT_QUESTION, extra_payload)]

    elif 8 <= num_answers < 12:
        # We collect your answers, show results
        result_page_msg = 'Se svarene i detalj og hvilke løfter som hører til på din egen resultatside'
        more_cats_msg = 'Du kan se svarene dine fra menyen når som helst. Velg nytt tema for å gjøre ditt resultat mer presist.'
        image_url = 'https://data.holderdeord.no/assets/og_logo-8b1cb2e26b510ee498ed698c4e9992df.png'
        replies += [
            format_text(sender_id, next_text),
            format_vg_result_reply(sender_id, session),
            # FIXME: Voter guide results
            format_generic_simple(sender_id, result_page_msg, format_quiz_result_button(session), image_url=image_url),
            format_quick_reply_with_intent(
                sender_id, 'Neste tema!', more_cats_msg, intents.INTENT_NEXT_QUESTION, extra_payload)]
    else:
        # Next manuscript
        replies += [format_quick_reply_with_intent(
            sender_id, 'Neste tema!', next_text, intents.INTENT_NEXT_QUESTION, extra_payload)]

    return replies


def get_next_vg_question_reply(sender_id, session, payload):
    # Link to an unanswered and not skipped manuscript in the same category
    next_text = "Når du er klar kan du gå videre til neste spørsmål"
    next_manuscript = get_next_manuscript(session)
    extra_payload = {'manuscript': next_manuscript.pk if next_manuscript else None}
    return format_quick_reply_with_intent(sender_id, "Neste spørsmål", next_text, intents.INTENT_NEXT_QUESTION, extra_payload)


def get_vg_result(sender_id, session, payload):
    return [format_vg_result_reply(sender_id, session), get_next_vg_question_reply(sender_id, session, payload)]


def get_answer_replies(sender_id, session, payload):
    extra_payload = {'manuscript': Manuscript.objects.get_default(default=Manuscript.DEFAULT_QUIZ).pk}
    if not hasattr(session, 'answers') or session.answers is None:
        no_results_msg = '🤔 Du har ikke svart på noe enda... Velg et tema'
        return [format_quick_reply_with_intent(
            sender_id, 'Okey 👍', no_results_msg, intents.INTENT_RESET_SESSION, extra_payload)]

    msg = 'Se svarene i detalj og hvilke løfter som hører til på din egen resultatside'
    ready_msg = 'Klar for å gå videre?'
    image_url = 'https://data.holderdeord.no/assets/og_logo-8b1cb2e26b510ee498ed698c4e9992df.png'

    return [
        format_quiz_result_reply(sender_id, session),
        format_generic_simple(sender_id, msg, format_quiz_result_button(session), image_url=image_url),
        format_quick_reply_with_intent(sender_id, 'Videre', ready_msg, intents.INTENT_RESET_SESSION, extra_payload)]
