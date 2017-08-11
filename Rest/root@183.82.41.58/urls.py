# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include

from django.conf import settings
from django.conf.urls.static import static

from snippets import views
from snippets.views import *


urlpatterns = [
   
	url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),

	url(r'^testrequests/$', views.RequestList.as_view(), name='testrequest-list'),
    url(r'^testrequests/(?P<pk>[0-9]+)/$', views.RequestDetail.as_view(), name='testrequest-detail'),

	url(r'^project/$', views.ProjectList.as_view()),
    url(r'^project/(?P<pk>[0-9]+)/$', views.ProjectDetail.as_view()),
    url(r'^testcase/$', views.TestCaseList.as_view()),
    url(r'^testcase/(?P<pk>[0-9]+)/$', views.TestCaseDetail.as_view()),
    
   ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
