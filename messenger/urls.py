from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.AdminActionsView.as_view(), name='admin-actions'),
    url(r'^webhook$', views.webhook, name='webhook'),
    url(r'^updatemenu/$', views.bot_profile_update, name='bot-profile-update')
]
