from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from oauth2client.contrib.django_util.site import urls as oauth2_urls

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='messenger_bot:admin-actions'), name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^messenger/', include('messenger_bot.urls', namespace='messenger_bot')),
    url(r'^quiz/', include('quiz.urls', namespace='quiz')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^oauth2/', include(oauth2_urls)),  # For sync
    url(r'^oauth/', include('social_django.urls', namespace='social'))  # For social login
]
