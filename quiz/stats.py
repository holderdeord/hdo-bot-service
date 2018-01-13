from django.db.models import Count

from quiz.models import AnswerSet, QuizAnswer
from django.db.models.functions import TruncDate


def counts_per_day(model=AnswerSet):

    answer_sets = model.objects.annotate(day=TruncDate('created')) \
        .values('day') \
        .annotate(count=Count('id')) \
        .values_list('day', 'count')

    return sorted(map(lambda _as: [_as[0].isoformat(), _as[1]], answer_sets))

