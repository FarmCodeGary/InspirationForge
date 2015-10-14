from django.conf.urls import url

from . import views, feeds

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^page/(?P<page>[0-9]+)$', views.IndexView.as_view(),
        name='indexpage'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<slug>[a-z0-9_-]+)/$',
        views.ArticleView.as_view(), name='article'),
    url(r'^tag/(?P<slug>[a-z0-9_-]+)/$', views.TagView.as_view(),
        name='tag'),
    url(r'^feed/$', feeds.LatestArticlesFeed(), name='rssfeed'),
]

