
"""USAS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1/. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from usasui.views import file_upload,home,StateListView,RunTest,add_records,ChartData,HomeView,get_data

from usasui.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$',home, name='home'),
    url(r'^upload/$',file_upload,name='file_upload'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^(?P<status>[A-Z]{1})/$', StateListView.as_view(),name="status_sort"),
    url(r'^runtest/(?P<pk>[0-9]+)/$', RunTest, name='runtest'),
    url(r'^add_records/$',add_records, name='add_records'),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^api/chart/data$', ChartData.as_view()),
    url(r'^api/data/$', get_data, name='api-data'),
    url(r'^add_project/$',project_addition,name='add_project'),
    url(r'^testcase_addition/$',testcase_addition,name='testcase_addition'),
    url(r'^testplan/$',testplan,name='testplan'),
    url(r'^get_project_case/$',get_project_case,),
    url(r'^get_robot/$',get_robot,),

    url(r'^rest/testrequests/$', RequestList.as_view(), name='testrequest-list'),
    url(r'^rest/testrequests/(?P<pk>[0-9]+)/$', RequestDetail.as_view(), name='testrequest-detail'),

    url(r'^rest/project/$', ProjectList.as_view()),
    url(r'^rest/project/(?P<pk>[0-9]+)/$', ProjectDetail.as_view()),
    url(r'^rest/testcase/$', TestCaseList.as_view()),
    url(r'^rest/testcase/(?P<pk>[0-9]+)/$', TestCaseDetail.as_view()),
    url(r'^rest/testrun/$', TestRunList.as_view()),
    url(r'^rest/testreport/$', TestReportList.as_view({'get': 'list'})),
    url(r'^rest/testview/$', TextView.as_view()),
    url(r'^rest/resultlog/$', ResultLogView.as_view()),
    url(r'^rest/resultview/$', ResultView.as_view()),
    url(r'^rest/reportview/$', TestReportView.as_view()),
    url(r'^get_project/$',get_project,name='get_project'),
    #url(r'^rest/', include('snippets.urls')),

    url(r'^dashbord/$',dashbord,name='dashbord'),      
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))


    # url(r'^login/$', 'django.contrib.auth.views.login'),
    # url(r'^logout/$', 'django.contrib.auth.views.logout'),
    #--------------------------------------------------------------->
    url(r'^rest/report/$',Report.as_view(), name='my_rest_view'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
