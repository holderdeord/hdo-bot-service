import json
import logging

from messenger.api import send_message
from messenger.api.formatters import format_text
from messenger.chat import get_replies
from messenger.intents import INTENT_RESET_SESSION
from messenger.models import ChatSession
from messenger.utils import render_and_load_manuscript
from quiz.models import Manuscript

logger = logging.getLogger(__name__)


def _has_quick_reply_payload(event):
    return 'message' in event and 'quick_reply' in event['message'] and 'payload' in event['message']['quick_reply']


def received_event(event):
    # TODO: Add Sender Action "..." to let the user know we are processing the request
    sender_id = event['sender']['id']
    logger.debug('in received_message: {}'.format(event))

    # Is new session?
    session = ChatSession.objects.filter(user_id=sender_id).first()
    if not session:
        # NEW
        session = init_or_reset_session(sender_id)

    # Has payload?
    payload = None
    if 'postback' in event:
        payload = json.loads(event['postback']['payload'])
    elif _has_quick_reply_payload(event):
        payload = json.loads(event['message']['quick_reply']['payload'])

    if payload and payload['intent'] == INTENT_RESET_SESSION:
        # Reset session
        logger.debug("Reseting session.user_id={}".format(sender_id))
        session = init_or_reset_session(sender_id, session)

    # Get one or more replies
    replies = get_replies(sender_id, session, payload)

    # Update session state
    session.save()

    # Send replies
    for reply in replies:
        logger.debug("send_message({})".format(reply))
        send_message(reply)


def init_or_reset_session(sender_id, session=None):
    m_initial = Manuscript.objects.get_default()
    if not m_initial:
        msg = "No manuscripts, bailing..."
        send_message(format_text(sender_id, msg))
        raise Exception(msg)

    # Serialize what we need and put in the session state
    meta = {
        'manuscript': render_and_load_manuscript(m_initial),
        'item': 0,
        'promise': 0,
        'first_name': ''
    }

    # Existing?
    if session is not None:
        session.meta = meta
        session.save()
        return session

    return ChatSession.objects.create(user_id=sender_id, meta=meta)
