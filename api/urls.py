from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from .views.manuscript import ManuscriptView, ManuscriptDetailView, CategoryRetrieveView, ManuscriptListView

router = SimpleRouter()


urlpatterns = [
    url(r'^manuscripts/(?P<pk>\d+)/$', ManuscriptDetailView.as_view(), name='manuscript-detail'),
    url(r'^manuscripts/$', ManuscriptListView.as_view(), name='manuscript-list'),
    url(r'^categories/(?P<pk>\d+)/$', CategoryRetrieveView.as_view(), name='category-detail'),
    url(r'^categories/(?P<category_id>\d+)/manuscript/(?P<manuscript_id>\d+)?$',
        ManuscriptView.as_view(),
        name='manuscript-random-in-category'),
] + router.urls
