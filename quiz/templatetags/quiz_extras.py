import json

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.template import Library
from django.utils.safestring import mark_safe
from quiz.models import AnswerSet
from quiz.utils import PARTY_SHORT_NAME_SLUGS

register = Library()


@register.simple_tag(name='correct_answers_js')
def correct_answers_js(answers, var_name):
    # Note: chart.js does not have a default color pallette
    color_palette = [
        '#858fa3',
        '#5cb85c',
    ]

    if isinstance(answers, AnswerSet):
        answers = AnswerSet.objects.filter(pk=answers.pk)

    counts = answers.correct_answers()
    data = {
        'labels': [],
        'datasets': [{
            'data': [],
            'backgroundColor': color_palette + color_palette + color_palette
        }]
    }
    for c in counts:
        data['labels'].append(' {}'.format(c['answers__correct_status']))
        data['datasets'][0]['data'].append(c['correct'])

    return mark_safe('var {} = JSON.parse(\'{}\')'.format(var_name, json.dumps(data)))


@register.simple_tag
def get_party_image_url(party):
    slug = PARTY_SHORT_NAME_SLUGS.get(party)
    if not slug:
        return ''

    return static('quiz/images/{}.png'.format(slug))
