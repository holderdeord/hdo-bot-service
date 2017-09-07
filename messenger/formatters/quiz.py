import json
import random

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse

from messenger import intents
from messenger.api.formatters import format_quick_replies, format_text
from quiz.models import Promise, QuizAnswer
from quiz.templatetags.quiz_extras import get_party_image_url
from quiz.utils import PARTY_SHORT_NAMES


def format_quiz_alternatives(recipient_id, manus):
    buttons = []
    alts = manus['quiz_alternatives']
    random.shuffle(alts)

    for alt in alts:
        buttons.append({
            "content_type": "text",
            "title": PARTY_SHORT_NAMES[alt['text']],
            "payload": json.dumps({
                'alternative': alt['pk'],
                'intent': intents.INTENT_ANSWER_QUIZ_QUESTION
            }),
            "image_url": get_party_image_url(alt['text'], image_dir='images_white')
        })

    return format_quick_replies(recipient_id, buttons, manus['name'])


def format_quiz_answer_button(answer):
    res_url = '{}{}'.format(settings.BASE_URL, reverse('quiz:quiz-answer-detail', args=[answer.uuid]))
    return [
        {
            "type": "web_url",
            "url": res_url,
            "title": "Vis svaret",
        },
    ]


def format_quiz_result_reply(sender_id, session):
    alts = QuizAnswer.objects.filter(answer_set__session=session)

    your_count = alts.filter(quiz_alternative__correct_answer=True).count()
    total_count = alts.count()
    percent = (your_count / total_count) * 100

    text = 'Du har {:.1f}% riktig, det vil si {} av {}.'.format(percent, your_count, total_count)
    return format_text(sender_id, text)


def format_broken_question(recipient_id, question, question_text):
    buttons = [
        {
            "content_type": 'text',
            "title": 'Holdt',
            "payload": json.dumps({
                'question': question['pk'],
                'answer': Promise.FULFILLED,
                'intent': intents.INTENT_ANSWER_QUIZ_BROKEN_QUESTION,
             }),
            "image_url": static('messenger/icon_fulfilled.png')
        },
        {
            "content_type": 'text',
            "title": 'Brutt',
            "payload": json.dumps({
                'question': question['pk'],
                'answer': Promise.BROKEN,
                'intent': intents.INTENT_ANSWER_QUIZ_BROKEN_QUESTION,
             }),
            "image_url": static('messenger/icon_broken.png')
        }
    ]

    return format_quick_replies(recipient_id, buttons, question_text)
