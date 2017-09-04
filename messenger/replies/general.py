import logging

from django.conf import settings

from messenger.api import send_message
from messenger.api.formatters import format_text
from messenger.formatters.general import format_reset_answer, format_quick_replies_with_intent
from messenger.formatters.quiz import format_question
from messenger.intents import (INTENT_ANSWER_QUIZ_QUESTION, INTENT_GET_HELP, INTENT_RESET_SESSION, INTENT_GET_STARTED,
                               INTENT_GOTO_MANUSCRIPT, INTENT_ANSWER_VG_QUESTION, INTENT_NEXT_ITEM,
                               INTENT_RESET_ANSWERS, INTENT_RESET_ANSWERS_CONFIRM, INTENT_NEXT_QUESTION,
                               INTENT_VG_CATEGORY_SELECT, INTENT_SHOW_ANSWERS)
from messenger.replies.quiz import get_quiz_question_replies, get_quiz_level_replies
from messenger.replies.voter_guide import (get_vg_category_replies, get_vg_questions,
                                           get_vg_question_replies, get_vg_result, get_vg_answer_replies)
from messenger.utils import delete_answers, save_vg_answer, get_result_url
from quiz.models import ManuscriptItem

logger = logging.getLogger(__name__)


def get_replies(sender_id, session, payload=None):
    """ Look in session state and payload and format one or more replies to the user"""
    # FIXME: maybe this needs another abstraction level. Map from intent to get_replies function?
    replies = []

    if payload is not None:
        # User pressed a button or similiar
        intent = payload['intent']

        if intent in [INTENT_RESET_SESSION, INTENT_GET_STARTED, INTENT_GOTO_MANUSCRIPT, INTENT_NEXT_ITEM,
                      INTENT_NEXT_QUESTION]:
            # Do nothing and just keep going
            pass

        elif intent == INTENT_RESET_ANSWERS:
            return [format_reset_answer(sender_id)]

        elif intent == INTENT_RESET_ANSWERS_CONFIRM:
            delete_answers(session)
            return [format_text(sender_id, '💥💥💥 Svarene dine er slettet')]

        elif intent == INTENT_GET_HELP:
            replies += [format_text(sender_id, 'Ingen fare 😊 To setninger som forteller deg hvor du kan få hjelp ♿')]

        elif intent == INTENT_ANSWER_QUIZ_QUESTION:
            # Quiz: Answer replies
            replies += get_quiz_question_replies(sender_id, session, payload)

        elif intent == INTENT_SHOW_ANSWERS:
            # Show answers
            return get_vg_answer_replies(sender_id, session, payload)

        elif intent == INTENT_ANSWER_VG_QUESTION:
            # Voter guide: Answer replies
            save_vg_answer(session, payload)
            return get_vg_question_replies(sender_id, session, payload)

        elif intent == INTENT_VG_CATEGORY_SELECT:
            # Voter guide: Paged categories
            last_item = session.meta['manuscript']['items'][session.meta['item'] - 1]
            return get_vg_category_replies(sender_id, session, payload, last_item['text'])

        else:
            msg = "Error: Unknown intent '{}'".format(intent)
            logger.error(msg)
            if settings.DEBUG:
                send_message(format_text(sender_id, msg))

    manus = session.meta['manuscript']
    if session.meta['item'] >= len(manus['items']):
        return replies

    item = manus['items'][session.meta['item']]
    last_item = False

    # Text items (add until no more)
    while item['type'] == ManuscriptItem.TYPE_TEXT and session.meta['item'] < len(manus['items']):
        logger.debug("Adding text reply: [{}]".format(session.meta['item'] + 1))

        replies += [format_text(sender_id, item['text'])]
        session.meta['item'] += 1
        if session.meta['item'] < len(manus['items']):
            item = manus['items'][session.meta['item']]
        else:
            last_item = True

    # Quick replies
    if item['type'] == ManuscriptItem.TYPE_QUICK_REPLY:
        logger.debug("Adding quick reply: [{}]".format(session.meta['item'] + 1))

        replies += [format_quick_replies_with_intent(sender_id, item)]
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

        replies += [format_text(sender_id, get_result_url(session))]
        session.meta['item'] += 1

    # Quiz: Show level select
    elif item['type'] == ManuscriptItem.TYPE_Q_LEVEL_SELECT:
        logger.debug("Adding quiz level [{}]".format(session.meta['item'] + 1))

        replies += get_quiz_level_replies(sender_id, session, payload, item['text'])
        session.meta['item'] += 1

    # Quiz: Show category select
    elif item['type'] == ManuscriptItem.TYPE_Q_CATEGORY_SELECT:
        logger.debug("Adding quiz category select [{}]".format(session.meta['item'] + 1))

        # TODO: Link to quiz question instead of voter guide questions
        # TODO: Filter by level (taken from payload['level'])
        replies += get_vg_category_replies(sender_id, session, payload, item['text'])
        session.meta['item'] += 1

    # Voter guide: Show category select
    elif item['type'] == ManuscriptItem.TYPE_VG_CATEGORY_SELECT:
        logger.debug("Adding voter guide categories [{}]".format(session.meta['item'] + 1))

        replies += get_vg_category_replies(sender_id, session, payload, item['text'])
        session.meta['item'] += 1

    # Voter guide: Show questions
    elif item['type'] == ManuscriptItem.TYPE_VG_QUESTIONS:
        logger.debug("Adding voter guide questions [{}]".format(session.meta['item'] + 1))

        replies += get_vg_questions(sender_id, session, payload, item['text'])
        session.meta['item'] += 1

    # Voter guide: result
    elif item['type'] == ManuscriptItem.TYPE_VG_RESULT:
        logger.debug("Adding voter guide result [{}]".format(session.meta['item'] + 1))

        replies += get_vg_result(sender_id, session, payload)
        session.meta['item'] += 1

    # Do nothing for last items of type text
    elif last_item:
        pass

    # Unhandled
    else:
        msg = "Unhandled manuscript item type: {} [{}]".format(item['type'], session.meta['item'] + 1)
        logger.error(msg)
        if settings.DEBUG:
            send_message(format_text(sender_id, msg))

    # Handle last item and next_manuscript
    if not last_item and session.meta['item'] == len(manus['items']):
        last_item = True

    if last_item and manus['next']:
        session.meta['next_manuscript'] = manus['next']

    return replies
