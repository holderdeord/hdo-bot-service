from django.conf.urls import url

from accounts.views import ProfileView

urlpatterns = [
    url(r'^profile/$', ProfileView.as_view(), name='profile')
]
