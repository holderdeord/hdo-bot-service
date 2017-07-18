import logging

from django.conf import settings

from messenger.api import send_message
from messenger.api.formatters import format_text
from messenger.intent_formatters import format_question, format_quick_reply_with_intents, format_reset_answer
from messenger.intents import (INTENT_ANSWER_QUIZ_QUESTION, INTENT_GET_HELP, INTENT_RESET_SESSION, INTENT_GET_STARTED,
                               INTENT_GOTO_MANUSCRIPT, INTENT_ANSWER_VG_QUESTION, INTENT_NEXT_ITEM,
                               INTENT_RESET_ANSWERS, INTENT_RESET_ANSWERS_CONFIRM)
from messenger.replies.quiz import get_quiz_result_url, get_quiz_question_replies
from messenger.replies.voter_guide import (get_voter_guide_category_replies, get_voter_guide_questions,
                                           get_vg_question_replies, get_voter_guide_result)
from messenger.utils import delete_answers
from quiz.models import ManuscriptItem

logger = logging.getLogger(__name__)


def get_replies(sender_id, session, payload=None):
    """ Look in session state and payload and format one or more replies to the user"""
    # FIXME: maybe this needs another abstraction level. Map from intent to get_replies function?
    replies = []
    manus = session.meta['manuscript']
    if session.meta['item'] >= len(manus['items']):
        return []

    item = manus['items'][session.meta['item']]

    if payload is not None:
        # User pressed a button or similiar
        intent = payload['intent']

        if intent in [INTENT_RESET_SESSION, INTENT_GET_STARTED, INTENT_GOTO_MANUSCRIPT, INTENT_NEXT_ITEM]:
            # Do nothing and just keep going
            pass

        elif intent == INTENT_RESET_ANSWERS:
            return [format_reset_answer(sender_id)]

        elif intent == INTENT_RESET_ANSWERS_CONFIRM:
            delete_answers(session)
            return [format_text(sender_id, 'Nå har vi slettet alt :-) 💥')]

        elif intent == INTENT_GET_HELP:
            # FIXME: User is stuck
            return [format_text(sender_id, 'Ingen fare 😊 To setninger som forteller deg hvor du kan få hjelp ♿')]

        elif intent == INTENT_ANSWER_QUIZ_QUESTION:
            # Quiz: Answer replies
            replies += get_quiz_question_replies(sender_id, session, payload)

        elif intent == INTENT_ANSWER_VG_QUESTION:
            # Voting guide: Answer replies
            replies += get_vg_question_replies(sender_id, session, payload)

        else:
            msg = "Error: Unknown intent '{}'".format(intent)
            logger.error(msg)
            if settings.DEBUG:
                send_message(format_text(sender_id, msg))

    # Text items (add until no more)
    while item['type'] == ManuscriptItem.TYPE_TEXT and session.meta['item'] < len(manus['items']):
        logger.debug("Adding text reply: [{}]".format(session.meta['item'] + 1))

        replies += [format_text(sender_id, item['text'])]
        session.meta['item'] += 1
        if session.meta['item'] < len(manus['items']):
            # Last item in manuscript!
            item = manus['items'][session.meta['item']]

    # Quick replies
    if item['type'] == ManuscriptItem.TYPE_QUICK_REPLY:
        logger.debug("Adding quick reply: [{}]".format(session.meta['item'] + 1))

        replies += [format_quick_reply_with_intents(sender_id, item)]
        session.meta['item'] += 1

    # Quiz: Show checked promises question
    elif item['type'] == ManuscriptItem.TYPE_Q_PROMISES_CHECKED:
        if session.meta['promise'] == len(manus['promises']):
            # Last promise in checked promises quiz
            logger.debug("Last promise: [{}]".format(session.meta['item'] + 1))

            session.meta['item'] += 1
            replies += get_replies(sender_id, session)  # Add next item reply

        else:
            logger.debug("Adding promise reply: [{}]".format(session.meta['promise'] + 1))

            question = manus['promises'][session.meta['promise']]
            question_text = 'Løfte #{} {}'.format(session.meta['promise'] + 1, question['body'])

            replies += [format_question(sender_id, question, question_text)]
            session.meta['promise'] += 1

    # Quiz: Show results
    elif item['type'] == ManuscriptItem.TYPE_QUIZ_RESULT:
        logger.debug("Adding quiz result [{}]".format(session.meta['item'] + 1))

        replies += [format_text(sender_id, get_quiz_result_url(session))]
        session.meta['item'] += 1

    # Voter guide: Show category select
    elif item['type'] == ManuscriptItem.TYPE_VG_CATEGORY_SELECT:
        logger.debug("Adding voter guide categories [{}]".format(session.meta['item'] + 1))

        replies += get_voter_guide_category_replies(sender_id, session, payload, item['text'])
        session.meta['item'] += 1

    # Voter guide
    elif item['type'] == ManuscriptItem.TYPE_VG_QUESTIONS:
        logger.debug("Adding voter guide questions [{}]".format(session.meta['item'] + 1))

        replies += get_voter_guide_questions(sender_id, session, payload, item['text'])
        session.meta['item'] += 1

    # Voter guide
    elif item['type'] == ManuscriptItem.TYPE_VG_RESULT:
        logger.debug("Adding voter guide result [{}]".format(session.meta['item'] + 1))

        replies += get_voter_guide_result(sender_id, session, payload)
        session.meta['item'] += 1
    else:
        msg = "Unhandled manuscript item type: {} [{}]".format(item['type'], session.meta['item'] + 1)
        logger.error(msg)
        if settings.DEBUG:
            send_message(format_text(sender_id, msg))

    return replies
