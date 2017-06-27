from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from .views.manuscript import (ManuscriptView, ManuscriptDetailView, CategoryRetrieveView, ManuscriptListView,
                               CategoryListView)

router = SimpleRouter()


urlpatterns = [
    # Manuscripts
    url(r'^manuscripts/(?P<pk>\d+)/$', ManuscriptDetailView.as_view(), name='manuscript-detail'),
    url(r'^manuscripts/$', ManuscriptListView.as_view(), name='manuscript-list'),

    # Categories
    url(r'^categories/(?P<pk>\d+)/$', CategoryRetrieveView.as_view(), name='category-detail'),
    url(r'^categories/(?P<category_id>\d+)/manuscript/(?P<manuscript_id>\d+)?$',
        ManuscriptView.as_view(),
        name='manuscript-random-in-category'),
    url(r'^categories/$', CategoryListView.as_view(), name='categories-list'),

] + router.urls
