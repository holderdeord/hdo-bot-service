from django.conf.urls import url
from rest_framework.routers import SimpleRouter
from .views.manuscript import ManuscriptView

router = SimpleRouter()


urlpatterns = [
    url(r'^category/(?P<category_id>\d+)/manuscript/(?P<manuscript_id>\d+)?$',
        ManuscriptView.as_view(),
        name='api:manuscript'),
] + router.urls
