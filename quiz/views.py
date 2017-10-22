from django.conf import settings
from django.http import HttpResponse
from django.views.generic import DetailView

from oauth2client.contrib.django_util.decorators import oauth_enabled

from messenger.utils import count_and_sort_answers
from quiz.models import AnswerSet, VoterGuideAlternative, QuizAlternative, QuizAnswer


@oauth_enabled
def get_authorize_link(request):
    if request.oauth.has_credentials():
        return HttpResponse('Authorized!')

    return HttpResponse('Here is an OAuth Authorize link:<a href="{}">Authorize</a>'.format(
        request.oauth.get_authorize_redirect()))


class VoterGuideAnswerSetView(DetailView):
    model = AnswerSet
    context_object_name = 'answer_set'
    slug_field = 'uuid'
    template_name = 'voterguide/answerset_detail.html'

    def get_context_data(self, **kwargs):
        medals = {1: '🥇', 2: '🥈', 3: '🥉'}
        vg_alts = VoterGuideAlternative.objects.filter(answers__answer_set=self.object)
        vg_alts = vg_alts.order_by('manuscript__hdo_category__name')
        answers = count_and_sort_answers(vg_alts)
        total_count = vg_alts.count()

        vg_answers_sorted = []
        for i, item in enumerate(answers.items(), start=1):
            count, parties = item
            vg_answers_sorted.append({
                'count': count,
                'parties': parties,
                'rank': medals.get(i, '{}.'.format(i)),
                'percent': '{:.1f}%'.format((count / total_count) * 100)

            })

        return {
            'all_answers': AnswerSet.objects.all(),
            'totals': AnswerSet.objects.correct_answers(),
            'vg_answers_sorted': vg_answers_sorted,
            'vg_alts': vg_alts,
            'is_shared': self.request.GET.get('shared') == '1',
            'app_id': settings.FACEBOOK_APP_ID,
            'page_id': settings.FACEBOOK_PAGE_ID,
            **super().get_context_data(**kwargs)
        }


class QuizAnswerView(DetailView):
    model = QuizAnswer
    context_object_name = 'answer'
    slug_field = 'uuid'
    template_name = 'quiz/answer_detail.html'

    def get_context_data(self, **kwargs):
        alt = self.object.quiz_alternative
        return {
            'alternative': alt,
            'answer': self.object,
            'answer_set': self.object.answer_set,
            'manuscript': alt.manuscript
        }


class QuizAnswerSetView(DetailView):
    model = AnswerSet
    context_object_name = 'answer_set'
    slug_field = 'uuid'
    template_name = 'quiz/answerset_detail.html'

    def _populate_categories(self, answered_alts):
        cats = [alt.manuscript.hdo_category for alt in answered_alts if alt.manuscript.hdo_category is not None]
        categories = sorted(set(cats), key=lambda x: x.name)
        for category in categories:
            category.correct = answered_alts.filter(manuscript__hdo_category=category).filter(
                correct_answer=True).count()
            category.total = answered_alts.filter(manuscript__hdo_category=category).count()
        return categories

    def _populate_questions_and_alternatives(self, answered_alts, all_alts):
        questions = [alternative.manuscript for alternative in answered_alts]

        for question in questions:
            question.alternatives = all_alts.filter(manuscript=question)
            question.answered = answered_alts.filter(manuscript=question)
            question.answered_text = ', '.join(question.answered.values_list('text', flat=True))
            question.correct_alts = question.alternatives.filter(correct_answer=True)
            question.correct_alts_text = ', '.join(question.correct_alts.values_list('text', flat=True))
            question.correct = True
            for answer in question.answered:
                question.correct = question.correct and question.correct_alts.filter(pk=answer.pk).count() > 0
            question.table_class = "table-success" if question.correct else "table-danger"

        return questions

    def get_context_data(self, **kwargs):
        all_alts = QuizAlternative.objects.all()
        answered_alts = QuizAlternative.objects.filter(answers__answer_set=self.object)

        return {
            'all_alternatives': answered_alts.order_by('manuscript__hdo_category__name'),
            'categories': self._populate_categories(answered_alts),
            'correct_alternatives': answered_alts.filter(correct_answer=True),
            'questions': self._populate_questions_and_alternatives(answered_alts, all_alts),
            'is_shared': self.request.GET.get('shared') == '1',
            'app_id': settings.FACEBOOK_APP_ID,
            'page_id': settings.FACEBOOK_PAGE_ID,
            **super().get_context_data(**kwargs)
        }
