from django.conf.urls import url

from accounts.views import ProfileView, LoginSuccessView

urlpatterns = [
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^redirect/$', LoginSuccessView.as_view(), name='login-success')
]
