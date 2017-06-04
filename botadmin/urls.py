from django.conf.urls import url

from botadmin.views import ReactAppView

urlpatterns = [
    url(r'^$', ReactAppView.as_view(), name='react-app')
]
