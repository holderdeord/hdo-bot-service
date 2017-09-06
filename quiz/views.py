from django.conf import settings
from django.http import HttpResponse
from django.views.generic import DetailView

from oauth2client.contrib.django_util.decorators import oauth_enabled

from messenger.utils import count_and_sort_answers, populate_questions_and_alternatives, populate_categories
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

    def get_context_data(self, **kwargs):
        all_alts = QuizAlternative.objects.all()
        answered_alts = QuizAlternative.objects.filter(answers__answer_set=self.object)
        quiz_all_alternatives = answered_alts.order_by('manuscript__hdo_category__name')
        quiz_correct_alternatives = answered_alts.filter(correct_answer=True)
        questions = populate_questions_and_alternatives(answered_alts, all_alts)
        categories = populate_categories(answered_alts)
        return {
            'all_alternatives': quiz_all_alternatives,
            'categories': categories,
            'correct_alternatives': quiz_correct_alternatives,
            'questions': questions,
            'is_shared': self.request.GET.get('shared') == '1',
            'app_id': settings.FACEBOOK_APP_ID,
            'page_id': settings.FACEBOOK_PAGE_ID,
            **super().get_context_data(**kwargs)
        }
        # medals = {1: '🥇', 2: '🥈', 3: '🥉'}
        # vg_alts = VoterGuideAlternative.objects.filter(answers__answer_set=self.object)
        # vg_alts = vg_alts.order_by('manuscript__hdo_category__name')
        # answers = count_and_sort_answers(vg_alts)
        # total_count = vg_alts.count()
        #
        # vg_answers_sorted = []
        # for i, item in enumerate(answers.items(), start=1):
        #     count, parties = item
        #     vg_answers_sorted.append({
        #         'count': count,
        #         'parties': parties,
        #         'rank': medals.get(i, '{}.'.format(i)),
        #         'percent': '{:.1f}%'.format((count / total_count) * 100)
        #
        #     })

        # return {
        #     # 'all_answers': AnswerSet.objects.all(),
        #     # 'totals': AnswerSet.objects.correct_answers(),
        #     # 'vg_answers_sorted': vg_answers_sorted,
        #     # 'vg_alts': vg_alts,
        # }
