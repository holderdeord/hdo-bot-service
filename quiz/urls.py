from django.conf.urls import url

from quiz.views import get_authorize_link, VoterGuideAnswerSetView, QuizAnswerSetView

urlpatterns = [
    url(r'authorize/$', get_authorize_link, name='get-authorize-link'),
    url(r'quiz/(?P<slug>[0-9a-f-]+)/', QuizAnswerSetView.as_view(), name='quiz-answer-set-detail'),
    url(r'voter-guide/(?P<slug>[0-9a-f-]+)/', VoterGuideAnswerSetView.as_view(), name='voter-guide-answer-set-detail')
]
