from django.conf.urls import url

from quiz.views import get_authorize_link, AnswerSetView

urlpatterns = [
    url(r'authorize/$', get_authorize_link, name='get-authorize-link'),
    url(r'result/(?P<slug>[0-9a-f-]+)/', AnswerSetView.as_view(), name='answer-set-detail')
]
