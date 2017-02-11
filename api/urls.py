from django.conf.urls import url
from rest_framework.routers import SimpleRouter
from .views.manuscript import ManuscriptView, ManuscriptRetrieveView, CategoryRetrieveView

router = SimpleRouter()


urlpatterns = [
    url(r'^category/(?P<category_id>\d+)/manuscript/(?P<manuscript_id>\d+)?$',
        ManuscriptView.as_view(),
        name='manuscript'),
    url(r'^manuscripts/(?P<pk>\d+)/$',
        ManuscriptRetrieveView.as_view(),
        name='manuscript-detail'),
    url(r'^cateogires/(?P<pk>\d+)/$',
        CategoryRetrieveView.as_view(),
        name='category-detail'),
] + router.urls
