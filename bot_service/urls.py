from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.flatpages.views import flatpage
from oauth2client.contrib.django_util.site import urls as oauth2_urls

from messenger.views import AdminActionsView

urlpatterns = [
    url(r'^$', AdminActionsView.as_view(), name='index'),

    url(r'^messenger/', include('messenger.urls', namespace='messenger')),
    url(r'^quiz/', include('quiz.urls', namespace='quiz')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^botadmin/', include('botadmin.urls', namespace='botadmin')),

    url(r'^oauth2/', include(oauth2_urls)),  # For sync
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # For social login

    url(r'^admin/', admin.site.urls),
]

# Flatpages
urlpatterns += [
    url(r'^(?P<url>.*/)$', flatpage),
]
