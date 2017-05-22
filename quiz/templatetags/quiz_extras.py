import json

from django.template import Library
from django.utils.safestring import mark_safe

from quiz.models import AnswerSet

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
