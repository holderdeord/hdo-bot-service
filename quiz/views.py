from django.http import HttpResponse
from django.views.generic import DetailView

from oauth2client.contrib.django_util.decorators import oauth_enabled

from messenger.utils import count_and_sort_answers
from quiz.models import AnswerSet, VoterGuideAlternative


@oauth_enabled
def get_authorize_link(request):
    if request.oauth.has_credentials():
        return HttpResponse('Authorized!')

    return HttpResponse('Here is an OAuth Authorize link:<a href="{}">Authorize</a>'.format(
        request.oauth.get_authorize_redirect()))


class AnswerSetView(DetailView):
    model = AnswerSet
    context_object_name = 'answer_set'
    slug_field = 'uuid'

    def get_context_data(self, **kwargs):
        medals = {0: '🥇', 1: '🥈', 2: '🥉'}
        vg_alts = VoterGuideAlternative.objects.filter(answers__answer_set=self.object)
        vg_alts = vg_alts.order_by('manuscript__hdo_category__name')
        answers = count_and_sort_answers(vg_alts)
        with_medals = []
        for i, item in enumerate(answers.items()):
            count, parties = item
            medal = medals.get(i, '')
            with_medals.append({'count': count, 'parties': parties, 'medal': medal + ' ' if medal else medal})

        return {
            'all_answers': AnswerSet.objects.all(),
            'totals': AnswerSet.objects.correct_answers(),
            'vg_answers_sorted': with_medals,
            'vg_alts': vg_alts,
            **super().get_context_data(**kwargs)
        }
