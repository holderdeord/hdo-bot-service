from messenger.api.formatters import format_text
from messenger.intent_formatters import format_vg_categories, format_vg_alternatives, format_quick_reply_next
from quiz.models import Manuscript, VoterGuideAlternative

MAX_QUICK_REPLIES = 11


def get_voter_guide_category_replies(sender_id, session, payload, text):
    """ Show manuscripts of type voter guide as quick replies """
    # FIXME: Support paging of quick replies, for now just use random first 11
    manuscripts = Manuscript.objects.filter(type=Manuscript.TYPE_VOTER_GUIDE, is_first_in_category=True)
    manuscripts = manuscripts.order_by('?').select_related('hdo_category')[:MAX_QUICK_REPLIES]

    return [format_vg_categories(sender_id, manuscripts, text)]


def get_voter_guide_questions(sender_id, session, payload, text):
    manus = session.meta['manuscript']

    return [format_vg_alternatives(sender_id, manus['voter_guide_alternatives'], text)]


def get_vg_question_replies(sender_id, session, payload):
    # TODO: Save answer (one AnswerSet per session/sender_id and one voter guide answer per answer)
    # TODO: Format answer

    # Update answer state
    current_answers = session.meta.get('answers', [])
    current_answers += [payload['alternative']]
    session.meta['answers'] = current_answers

    alt = VoterGuideAlternative.objects.get(pk=payload['alternative'])

    return [format_text(sender_id, "Du svarte \'{}\'".format(alt.text))]


def get_voter_guide_result(sender_id, session, payload):
    # TODO Lookup and format answers
    return [format_quick_reply_next(sender_id, "Videre", 'TODO: Vis resultat')]
