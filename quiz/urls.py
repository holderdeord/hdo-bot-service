from django.conf.urls import url

from quiz.views import get_authorize_link

urlpatterns = [
    url(r'authorize/$', get_authorize_link, name='get-authorize-link')
]
