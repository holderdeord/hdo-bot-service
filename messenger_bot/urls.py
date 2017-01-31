from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^webhook', views.webhook, name='webhook'),
    url(r'^$', views.MessageUsView.as_view(), name='message-us')
]
