# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
from snippets.views import SnippetViewSet, UserViewSet,RequestList,RequestDetail, ProjectList,ProjectDetail
from rest_framework import renderers

from rest_framework.routers import DefaultRouter

from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='Pastebin API')


router = DefaultRouter()
router.include_format_suffixes = False
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users',views.UserViewSet)



snippet_list = SnippetViewSet.as_view({
	'get':'list',
	'post':'create'
	})

snippet_detail = SnippetViewSet.as_view({
	'get':'retrieve',
	'put':'update',
	'patch':'partial_update',
	'delete':'destroy'
	})

snippet_highlight = SnippetViewSet.as_view({
	'get':'highlight'
	},renderer_classes=[renderers.StaticHTMLRenderer])

user_list = UserViewSet.as_view({
	'get':'list'
	})

user_detail = UserViewSet.as_view({
	'get': 'retrieve'
	})

urlpatterns = [
    url(r'^snippets/$', snippet_list, name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
    url(r'^users/$', user_list, name='user-list'),
	url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
	url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),

	#url(r'^$', views.api_root),

	url(r'^', include(router.urls)),

	url(r'^schema/$', schema_view),

	url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_highlight, name='snippet-highlight'),

	url(r'^testrequests/$', views.RequestList.as_view(), name='testrequest-list'),
    url(r'^testrequests/(?P<pk>[0-9]+)/$', views.RequestDetail.as_view(), name='testrequest-detail'),

	url(r'^project/$', views.ProjectList.as_view()),
    url(r'^project/(?P<pk>[0-9]+)/$', views.ProjectDetail.as_view()),
    # url(r'^testrequests/(?P<pk>[0-9]+)/$', views.TestRequestHighlight.as_view(), name='testrequest-highlight'),
   ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)


