import json
import logging
import random

from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext as _
from rest_framework.renderers import JSONRenderer

from api.serializers.manuscript import BaseManuscriptSerializer
from messenger.graph_api import get_user_profile, send_message
from messenger.messages import (format_text, format_question, TYPE_ANSWER, format_quick_reply_next,
                                format_image_attachment, TYPE_HELP, TYPE_SESSION_RESET)
from messenger.models import ChatSession

from quiz.models import Manuscript, ManuscriptItem
from quiz.utils import save_answers

logger = logging.getLogger(__name__)


def get_replies(sender_id, session):
    replies = []
    manus = session.meta['manuscript']
    if session.meta['current_item'] >= len(manus['items']):
        return []

    item = manus['items'][session.meta['current_item']]

    while item['type'] == ManuscriptItem.TYPE_TEXT and session.meta['current_item'] < len(manus['items']):
        logger.debug("Adding text reply: {}".format(session.meta['current_item'] + 1))

        replies.append(format_text(sender_id, item['text']))
        session.meta['current_item'] += 1
        if session.meta['current_item'] < len(manus['items']):
            # Last item!
            item = manus['items'][session.meta['current_item']]

    if item['type'] == ManuscriptItem.TYPE_Q_PROMISES_CHECKED:
        if session.meta['current_promise'] < len(manus['promises']):
            logger.debug("Adding promise reply: {}".format(session.meta['current_promise'] + 1))

            question = manus['promises'][session.meta['current_promise']]
            question_text = 'Løfte #{} {}'.format(session.meta['current_promise'] + 1, question['body'])
            replies.append(format_question(sender_id, question, question_text, session.uuid))
            session.meta['current_promise'] += 1
        else:
            logger.debug("Last promise: {}".format(session.meta['current_item'] + 1))

            session.meta['current_item'] += 1

    elif item['type'] == ManuscriptItem.TYPE_QUICK_REPLY:
        logger.debug("Adding quick reply: {}".format(session.meta['current_item'] + 1))

        replies.append(format_quick_reply_next(sender_id, item['text'], item['reply_text_1'], session.uuid))
        session.meta['current_item'] += 1

    elif item['type'] == ManuscriptItem.TYPE_QUIZ_RESULT:
        logger.debug("Adding quiz result: {}".format(session.meta['current_item'] + 1))

        replies.append(get_quiz_result(sender_id, session))
        session.meta['current_item'] += 1

    return replies


def is_manuscript_complete(session):
    _is_last_item = session.meta['current_item'] >= len(session.meta['manuscript']['items']) - 1
    _is_last_promise = session.meta['current_promise'] >= len(session.meta['manuscript']['promises']) - 1

    return _is_last_item and _is_last_promise


def received_message(event):
    sender_id = event['sender']['id']
    logger.debug('in received_message: {}'.format(event))

    # Is new session?
    session = ChatSession.objects.filter(user_id=sender_id, state=ChatSession.STATE_IN_PROGRESS).first()
    if not session:
        # NEW
        session = init_session(sender_id)

    if 'message' in event and 'quick_reply' in event['message'] and 'payload' in event['message']['quick_reply']:
        payload = json.loads(event['message']['quick_reply']['payload'])
        # FIXME: Refactor this
        handle_answer(payload, sender_id, session)
        return

    # Send replies
    replies = get_replies(sender_id, session)

    # Update session
    session.save()

    for reply in replies:
        logger.debug("reply: {}".format(reply))
        send_message(reply)

    if is_manuscript_complete(session):
        session.state = ChatSession.STATE_COMPLETE
        session.save()


def init_session(sender_id):
    m_initial = Manuscript.objects.first()
    if not m_initial:
        msg = "No manuscripts, bailing..."
        send_message(format_text(sender_id, msg))
        raise Exception(msg)

    # Serialize what we need and put in the session state
    manus = json.loads(JSONRenderer().render(BaseManuscriptSerializer(m_initial).data).decode())
    meta = {
        'manuscript': manus,
        'current_item': 0,
        'current_promise': 0,
        'first_name': ''
    }

    return ChatSession.objects.create(user_id=sender_id, meta=meta)


def get_question_replies(sender_id, session, payload):
    # FIXME: quiz specific
    first_name = session.meta['first_name']
    if not first_name:
        first_name = session.meta['first_name'] = get_user_profile(sender_id)['first_name']

    # Get last asked promise
    p_i = session.meta['current_promise']
    if p_i > 0:
        p_i -= 1
    promise = session.meta['manuscript']['promises'][p_i]

    # Is answer correct?
    if payload['answer'] == promise['status']:
        text = 'Godt svar {} 🙂 Det løftet ble {}'.format(first_name, _(promise['status']))
    else:
        text = 'Beklager {} 😩  Det var ikke riktig, det løftet ble {}'.format(first_name, _(promise['status']))

    replies = [format_text(sender_id, text)]

    # Try to get a random image of correct type and display 1 out of 3 times
    images = list(filter(lambda x: x['type'] == promise['status'], session.meta['manuscript']['images']))
    if images and session.meta['current_promise'] % 3 == 0:
        image = random.choice(images)
        replies.append(format_image_attachment(sender_id, image['url']))

    # Is last promise?
    if session.meta['current_promise'] == len(session.meta['manuscript']['promises']):
        save_answers(session)
        replies += get_replies(sender_id, session)

    return replies


def get_quiz_result(sender_id, session: ChatSession):
    url = reverse('quiz:answer-set-detail', args=[session.answers.uuid])
    return [format_text(sender_id, '{}{}'.format(settings.BASE_URL, url))]


def received_postback(event):
    payload = json.loads(event['postback']['payload'])
    sender_id = event['sender']['id']
    logger.debug('in recieved_postback: {}'.format(payload))
    if payload.get('type') == TYPE_HELP:
        send_message(format_text(sender_id, 'Ingen fare 😊 To setninger som forteller deg hvor du kan få hjelp ♿'))
        return

    if payload.get('type') == TYPE_SESSION_RESET:
        # Set current all current sessions complete
        current_sessions = ChatSession.objects.filter(
            user_id=sender_id, state=ChatSession.STATE_IN_PROGRESS)
        current_sessions.update(state=ChatSession.STATE_COMPLETE)

        # Pretend this is the first message to start a new session immediately
        # received_message(event)


def handle_answer(payload, sender_id, session):
    if is_manuscript_complete(session):
        session.state = ChatSession.STATE_COMPLETE
        session.save()

    replies = []
    # Add answer replies
    if payload.get('type') == TYPE_ANSWER:
        replies = get_question_replies(sender_id, session, payload)

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


def _update_answer_state(payload, session):
    current_answers = session.meta.get('answers', {})
    current_answers[payload['question']] = payload['answer']
    session.meta['answers'] = current_answers
