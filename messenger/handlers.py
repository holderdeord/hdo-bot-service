import json
import logging

from messenger.api import send_message
from messenger.intents import INTENT_RESET_SESSION, INTENT_GOTO_MANUSCRIPT, INTENT_NEXT_QUESTION
from messenger.models import ChatSession
from messenger.replies.general import get_replies
from messenger.utils import init_or_reset_session

logger = logging.getLogger(__name__)


def _has_quick_reply_payload(event):
    return 'message' in event and 'quick_reply' in event['message'] and 'payload' in event['message']['quick_reply']


def received_event(event, session=None, next_manuscript=None):
    # TODO: Maybe add Sender Action "..." to let the user know we are processing the request
    sender_id = event['sender']['id']
    logger.debug('in received_message: {}'.format(event))

    if session is None:
        # Is new session?
        session = ChatSession.objects.filter(user_id=sender_id).first()
        if not session:
            # NEW
            session = init_or_reset_session(sender_id)

    # Has payload?
    payload = None
    if next_manuscript is not None:
        pass
    elif 'postback' in event:
        payload = json.loads(event['postback']['payload'])
    elif _has_quick_reply_payload(event):
        payload = json.loads(event['message']['quick_reply']['payload'])

    # Reset or switch?
    init_or_reset_intents = [INTENT_RESET_SESSION, INTENT_GOTO_MANUSCRIPT, INTENT_NEXT_QUESTION]
    if next_manuscript or (payload and payload['intent'] in init_or_reset_intents):
        # Reset session with given manuscript (or default)
        logger.debug("Resetting session.user_id={}".format(sender_id))
        if next_manuscript is None:
            next_manuscript = payload.get('manuscript')
        session = init_or_reset_session(sender_id, session, next_manuscript)

    # Get one or more replies
    replies = get_replies(sender_id, session, payload)

    # Update session state
    session.save()

    # Send replies
    for reply in replies:
        logger.debug("send_message({})".format(reply))
        send_message(reply)

    # Should we loop?
    if session.meta.get('next_manuscript'):
        next_manuscript = session.meta.pop('next_manuscript')
        received_event(event, session, next_manuscript)
