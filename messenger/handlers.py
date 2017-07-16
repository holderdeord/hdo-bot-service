import json
import logging

from messenger.api import send_message
from messenger.intents import INTENT_RESET_SESSION, INTENT_GOTO_MANUSCRIPT
from messenger.models import ChatSession
from messenger.replies.general import get_replies
from messenger.utils import init_or_reset_session

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

    if payload and payload['intent'] in [INTENT_RESET_SESSION, INTENT_GOTO_MANUSCRIPT]:
        # Reset session with given manuscript (or default)
        logger.debug("Reseting session.user_id={}".format(sender_id))
        session = init_or_reset_session(sender_id, session, payload.get('manuscript'))

    # Get one or more replies
    replies = get_replies(sender_id, session, payload)

    # Update session state
    session.save()

    # Send replies
    for reply in replies:
        logger.debug("send_message({})".format(reply))
        send_message(reply)

