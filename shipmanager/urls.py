from django.conf.urls import patterns, url
from django.contrib import admin
from shipmanager import views

urlpatterns = patterns('',
    url(r'^$', views.search, name='search'),
    url(r'^index/$', views.index, name='index'),
    url(r'^regist/$', views.regist, name='regist'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^jump/$', views.jump, name='jump'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search_detail/$', views.search_detail, name='search_detail'),
    url(r'^news/$', views.News.as_view(), name='News'),
    url(r'^archive/(?P<year>\d+)/(?P<month>\d+)$', views.ArchiveView.as_view(), name='archive'),
    url(r'^article/(?P<article_id>\d+)$', views.ArticleDetailView.as_view(), name='detail'),
    url(r'^article/(?P<article_id>\d+)/comment/$', views.CommentPostView.as_view(), name='comment'),
    url(r'^personal/$', views.personal, name='personal'),
    url(r'^check/$', views.check, name='check'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^loginsuccess/$', views.loginsuccess, name='loginsuccess'),
    url(r'^logfail/$', views.logfail, name='logfail'),
)
