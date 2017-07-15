import json
import logging

from api.serializers.manuscript import BaseManuscriptSerializer
from messenger.api import send_message
from messenger.api.formatters import format_text
from messenger.chat import get_replies, get_quiz_question_replies
from messenger.intents import INTENT_GET_HELP, INTENT_RESET_SESSION, INTENT_ANSWER_QUIZ_QUESTION
from messenger.models import ChatSession
from messenger.utils import render_and_load_serializer_data
from quiz.models import Manuscript

logger = logging.getLogger(__name__)


# TODO: Simplify this
# - move json loads to helper functions
# - webhook message's can have payloads with types


def _has_quick_reply_payload(event):
    return 'message' in event and 'quick_reply' in event['message'] and 'payload' in event['message']['quick_reply']


def received_message(event):
    # TODO: Add Sender Action "..." to let the user know we are processing the request
    sender_id = event['sender']['id']
    logger.debug('in received_message: {}'.format(event))

    # Is new session?
    session = ChatSession.objects.filter(user_id=sender_id, state=ChatSession.STATE_IN_PROGRESS).first()
    if not session:
        # NEW
        session = init_session(sender_id)

    if _has_quick_reply_payload(event):
        payload = json.loads(event['message']['quick_reply']['payload'])
        # TODO: YOU ARE HERE
        # TODO: Refactor this, move it into get_replies
        handle_answer(payload, sender_id, session)
        return

    # Get one or more replies
    replies = get_replies(sender_id, session)

    # Update session state
    session.save()

    # Send replies
    for reply in replies:
        logger.debug("reply: {}".format(reply))
        send_message(reply)

    # check for script completion
    if is_manuscript_complete(session):
        session.state = ChatSession.STATE_COMPLETE
        session.save()


def received_postback(event):
    payload = json.loads(event['postback']['payload'])
    sender_id = event['sender']['id']
    logger.debug('in recieved_postback: {}'.format(payload))

    if payload['intent'] == INTENT_GET_HELP:
        send_message(format_text(sender_id, 'Ingen fare 😊 To setninger som forteller deg hvor du kan få hjelp ♿'))
        return

    if payload['intent'] == INTENT_RESET_SESSION:
        # Set current session complete
        # FIXME: This should point session.current_manuscript to default manuscript and show first message
        current_sessions = ChatSession.objects.filter(
            user_id=sender_id, state=ChatSession.STATE_IN_PROGRESS)
        current_sessions.update(state=ChatSession.STATE_COMPLETE)

        # Pretend this is the first message to start a new session immediately
        # received_message(event)


def init_session(sender_id):
    m_initial = Manuscript.objects.get_default()
    if not m_initial:
        msg = "No manuscripts, bailing..."
        send_message(format_text(sender_id, msg))
        raise Exception(msg)

    # Serialize what we need and put in the session state
    serializer = BaseManuscriptSerializer(m_initial)
    meta = {
        'manuscript': render_and_load_serializer_data(serializer),
        'current_item': 0,
        'current_promise': 0,
        'first_name': ''
    }

    return ChatSession.objects.create(user_id=sender_id, meta=meta)


def is_manuscript_complete(session):
    _is_last_item = session.meta['current_item'] >= len(session.meta['manuscript']['items']) - 1
    _is_last_promise = session.meta['current_promise'] >= len(session.meta['manuscript']['promises']) - 1

    return _is_last_item and _is_last_promise


def _update_answer_state(payload, session):
    current_answers = session.meta.get('answers', {})
    current_answers[payload['question']] = payload['answer']
    session.meta['answers'] = current_answers


def handle_answer(payload, sender_id, session):
    if is_manuscript_complete(session):
        session.state = ChatSession.STATE_COMPLETE
        session.save()

    replies = []
    # Get quiz answer replies
    if payload['intent'] == INTENT_ANSWER_QUIZ_QUESTION:
        replies = get_quiz_question_replies(sender_id, session, payload)

        _update_answer_state(payload, session)

    replies += get_replies(sender_id, session)

    # Update session
    session.save()

    for reply in replies:
        logger.debug("reply: {}".format(reply))
        send_message(reply)

    if is_manuscript_complete(session):
        session.state = ChatSession.STATE_COMPLETE
        session.save()
