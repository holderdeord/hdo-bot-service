import logging
import random

from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext as _

from messenger.api import get_user_profile
from messenger.api.formatters import format_text, format_image_attachment
from messenger.intent_formatters import format_question, format_quick_reply_next
from messenger.models import ChatSession

from quiz.models import ManuscriptItem
from quiz.utils import save_answers

logger = logging.getLogger(__name__)


def get_replies(sender_id, session):
    """ Look in session state and figure what to reply the user with"""
    # TODO: move quiz_1 and quiz_2 specific handlers to it's own file
    # TODO: Add voter_guide handlers (own file)
    # TODO: maybe this needs another abstraction level?
    replies = []
    manus = session.meta['manuscript']
    if session.meta['current_item'] >= len(manus['items']):
        return []

    item = manus['items'][session.meta['current_item']]

    # Text items (add until no more)
    while item['type'] == ManuscriptItem.TYPE_TEXT and session.meta['current_item'] < len(manus['items']):
        logger.debug("Adding text reply: {}".format(session.meta['current_item'] + 1))

        replies.append(format_text(sender_id, item['text']))
        session.meta['current_item'] += 1
        if session.meta['current_item'] < len(manus['items']):
            # Last item!
            item = manus['items'][session.meta['current_item']]

    # Quiz: Show checked promises question
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

    # Quick replies
    elif item['type'] == ManuscriptItem.TYPE_QUICK_REPLY:
        logger.debug("Adding quick reply: {}".format(session.meta['current_item'] + 1))

        replies.append(format_quick_reply_next(sender_id, item['text'], item['reply_text_1'], session.uuid))
        session.meta['current_item'] += 1

    # Quiz: Show results
    elif item['type'] == ManuscriptItem.TYPE_QUIZ_RESULT:
        logger.debug("Adding quiz result: {}".format(session.meta['current_item'] + 1))

        replies.append(get_quiz_result(sender_id, session))
        session.meta['current_item'] += 1

    return replies


def get_quiz_result(sender_id, session: ChatSession):
    url = reverse('quiz:answer-set-detail', args=[session.answers.uuid])
    return [format_text(sender_id, '{}{}'.format(settings.BASE_URL, url))]


def get_quiz_question_replies(sender_id, session, payload):
    """ Get replies to postback.type=TYPE_ANSWER """
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
