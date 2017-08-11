
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from django.core.management import call_command
from usasui.utils import get_output_dir, get_free_envs
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
#class based view login required (LoginRequiredMixin)

from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import View

from .forms import TestRequestForm, ProjectForm, TestCaseForm, TestRunForm
from .models import TestRequest, Project,TestSuit,TestCase,TestRun, TestReport
from datetime import datetime

from django.http import JsonResponse

#Get Robot attachement from JIRA 
 
import os
from jira.client import JIRA
from robot.api import ExecutionResult, ResultVisitor
import uuid
import json


def get_test_id():
    test_id = str(uuid.uuid4())[:11].replace('-', '').lower()
    #test_id = '9f16a22615'
    try:
        id_exists = TestRequest.objects.get(test_run_id=test_id)
        get_test_id()
    except:
        return test_id


def add_records(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TestRequestForm(request.POST, request.FILES)
        print request.POST
        # check whether it's valid:
        print form.is_valid()
        if form.is_valid():
            # process the data in form.cleaned_data as required
            instance = form.save(commit=False)
            instance.test_run_id = get_test_id()
            instance.save()
            # redirect to a new URL:
            return HttpResponseRedirect('.')

    # if a GET (or any other method) we'll create a blank form
    else:
        default_data = {'status': TestRequest.WAITING}
        form = TestRequestForm(default_data)
        
    return render(request, 'test-suit-upload.html', {'form': form})

def RunTest(request, pk=None):
    test_record = TestRequest.objects.get(pk=pk)
    test_record.status = TestRequest.TESTING
    test_record.save()
    free_envs = get_free_envs()
    if free_envs:
        logpath = get_output_dir((free_envs[0],test_record.test_file.file.name))
    else:
        return HttpResponseRedirect(reverse('status_sort', args=('C',)))
    print(logpath + 'from views')
    test_record.status = TestRequest.COMPLETED
    test_record.envt = free_envs[0].split('/')[::-1][1]
    print(free_envs[0].split('/')[::-1])
    test_record.log_path = '/media/' + logpath.split('/')[::-1][0]+'/log.html'
    xml_path = os.path.dirname(os.path.abspath(__file__)).split('NUTAS',1)[0] + 'NUTAS/UI/USAS/media/' + logpath.split('/')[::-1][0]+'/output.xml'
    result = ExecutionResult(xml_path)
    stats = result.statistics
    if stats.total.critical.failed:
        test_record.result = 'Failed'
    else:
        test_record.result = 'Passed'
    test_record.execution = datetime.now()
    test_record.save()
    return HttpResponseRedirect(reverse('status_sort', args=('C',)))

    
def home(request):
    return render(request, 'charts.html', {})


def file_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'file_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'file_upload.html',{})




class StateListView(LoginRequiredMixin,ListView):
    model = TestRequest
    template_name = 'test-activity.html'
    #template_name = 'test_request.html'
    context_object_name = 'test_by_status'

    def get_queryset(self):
        status_list = self.kwargs['status']
        return TestRequest.objects.filter(status=status_list).order_by('-id')


    def get_context_data(self, **kwargs):
        context = super(StateListView, self).get_context_data(**kwargs)
        context.update({'status': self.kwargs['status']})
        objects = context['test_by_status']
        paginator = Paginator(objects,10) 
        page = self.request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        context['test_by_status'] = contacts
        return context

#Chart 
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts.html', {})

import json
def get_data(request, *args, **kwargs):

    data = {
        "sales" : 100,
        "customers" : 10,
    }

    return JsonResponse(data)

class ChartData(APIView):
    
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        
        from django.db.models import Count
        DATE_FORMAT = "%Y-%m-%d"

        no_days = TestRequest.objects.filter().extra({'day':"Extract(day from created)"}).values_list('day').annotate(Count('id'))
        day_counts = [i[1] for i in no_days][::-1][:7]
        
        days_data = TestRequest.objects.all()
        day_created = [ i.created for i in days_data]
        days =list(set([i.strftime(DATE_FORMAT) for i in day_created]))
        last_seven_days  = days[:7]

        data = {
        "labels" : last_seven_days,
        "default" : day_counts,
        }
    
        return Response(data)



#-------------------------------------------------------------------------------------------

@login_required
def project_addition(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        print request.POST
        # check whether it's valid:
        print User
        print form.is_valid()
        if form.is_valid():
            # process the data in form.cleaned_data as required
            instance = form.save(commit=False)
            instance.user =  request.user
            print "ID :" + str(instance.id)
            instance.save()
            # redirect to a new URL:
            return HttpResponseRedirect('.')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProjectForm()
        
    # return render(request, 'add_project.html',{'form':form})
    return render(request, 'projects.html',{'form':form})


def testcase_addition(request):
    if request.method == 'POST':
        form = TestCaseForm(request.POST)
        print request.POST
        # check whether it's valid:
        print form.is_valid()
        if form.is_valid():
            # process the data in form.cleaned_data as required
            instance = form.save(commit=False)
            instance.save()
            # redirect to a new URL:
            return HttpResponseRedirect('.')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TestCaseForm()
        
    return render(request, 'test-suit.html',{'form':form})

def testplan(request):
    project = Project.objects.all()
    # print list(project)
    if request.method == 'POST':
        form = TestRunForm(request.POST)

        print request.POST
        # check whether it's valid:
        print form.is_valid()
        if form.is_valid():
            # process the data in form.cleaned_data as requireds
            instance = form.save(commit=False)
            ts_name = "test-suit-1"
            ts = TestSuit(name=ts_name)
            ts.save()
            instance.test_suit_name =ts
            # tq = TestRequest()
            instance.test_suit_name = ts
            project = form['project'].value() 
            #instance.project = TestCase.objects.filter(project=project)
            #instance.save()
            test_case_list = TestCase.objects.filter(project=project)
            print test_case_list
            instance.result = "No Run"
            instance.save()
            # redirect to a new URL:
            return HttpResponseRedirect('.')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TestRunForm()
        print form
        
    return render(request, 'schedule.html',{'form':form,'project':project})



#--------------------------------------------------------
def get_project_case(request):
    form = TestRun.objects.all()
    proj = Project.objects.filter(name=request.GET['project'])
    #test_case_list=TestCase.project.get(project=proj)
    tcl=proj[0].testcase_set.all()
    print tcl
    tl =[]
    for tc in tcl:
        tl.append(tc.testcase_id)
    print tl
    
    return HttpResponse(json.dumps(tl))

#-----------------------------------------------------------



#@login_required
def get_robot(request):
    if request.method == 'GET':
        # issue = request.GET.getlist('value[]')
        print "Get Data : ",request.GET.get('value[]')
        ts_name = request.GET.get('tsName')
        print "Test Suit Name Is :",ts_name
        value = request.GET.get('value[]')
        issue = value.split(",")
        print len(issue)
        #print "robot file path :",r_path
        #print type(str(r_path))
        if len(issue) > 0:

            url = settings.JIRA_URL
            username = settings.JIRA_USERNAME
            pwd = settings.JIRA_PWD
            print "%%%%%%%%%%%%%%%%%%%%%%"
            print url
            print username
            print pwd
            print "$$$$$$$$$$$$$$$$$$$"

            try:
                conn=JIRA(url, basic_auth =(username, pwd))
            except Exception as err:
                print "*****************"
                print err
                print "*****************"
                raise Exception(err)
            issue_list_conns=[ conn.issue(x)  for x in issue]
            
            f=open(os.path.join(settings.BASE_DIR,"media",''.join(map(str,issue_list_conns)))+".robot",'w')
            [ f.write(attach.get())  for x in issue_list_conns for attach in x.fields.attachment]
            
            project = Project.objects.all()[0]
            
            ts_rq = TestRequest(user=request.user,project=project,test_suit_id=ts_name,test_file=f.name)
            ts_rq.save()
            f.close() 
            # return HttpResponseRedirect(reverse('status_sort', args=('W',)))
            status = {'status':1,'message':"Successfully Inserted"}
            return  HttpResponse(json.dumps(status))

    return render(request, 'jira_testplan.html',{})


#------------------------
#login view
def login(request):

    return render(request,'registration/login.html',{})


#Charts  Dashboard

def dashbord(request):
    project = len(Project.objects.all())
    users = len(User.objects.all())
    test_case = len(TestCase.objects.all())
    test_run = len(TestRequest.objects.all())
    completed = len(TestRequest.objects.filter(status="C"))
    progress =  len(TestRequest.objects.filter(status="W"))

    #---------------Graph data from TestRequest ------

    from django.db.models import Count
    DATE_FORMAT = "%Y-%m-%d"

    no_days = TestRequest.objects.filter().extra({'day':"Extract(day from created)"}).values_list('day').annotate(Count('id'))
    day_counts = [i[1] for i in no_days][::-1][:7]
    
    days_data = TestRequest.objects.all()
    day_created = [ i.created for i in days_data]
    days =list(set([i.strftime(DATE_FORMAT) for i in day_created]))
    days = [x.replace('-','/') for x in days]
    last_seven_days  = days[:7]


    categories = last_seven_days
    ne_l =[]
    for p1 in last_seven_days:
        ne_l.append(str(p1.strip('\'')))
    data = day_counts
    context = {
        'project':project,
        'users' :users,
        'test_case' :test_case,
        'test_run':test_run,
        'categories_i':ne_l,
        'data_i' :data,
        'completed' :completed,
        'progress' :progress,

        }
    return render(request, 'dashboard1.html',context)

#---------------------------------------------------------------------------------------------------------

from models import TestRequest, Project, TestCase, TestRun
from serializers import TestRequestSerializer, ProjectSerializer, TestCaseSerializer, TestRunSerializer, TestReportSerializer, TestRequestSerializer, TestRequest2Serializer,TestRequest3Serializer,TestRequest4Serializer
from rest_framework import generics, viewsets
from rest_framework import permissions

class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly1,)
    permission_classes = (permissions.IsAdminUser,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class RequestList(generics.ListCreateAPIView):
    queryset = TestRequest.objects.all()
    serializer_class = TestRequestSerializer


class RequestDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly1,)
    permission_classes = (permissions.IsAdminUser,)
    queryset = TestRequest.objects.all()
    serializer_class = TestRequestSerializer

class TestCaseDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly1,)
    permission_classes = (permissions.IsAdminUser,)
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer

class TestCaseList(generics.ListCreateAPIView):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer

class TestRunList(generics.ListCreateAPIView):
    queryset = TestRun.objects.all()
    serializer_class = TestRunSerializer

class TestReportList(viewsets.ModelViewSet):
    queryset = TestReport.objects.all() 
    serializer_class = TestReportSerializer

from drf_multiple_model.views import MultipleModelAPIView

class TextView(MultipleModelAPIView):
    queryList = [
        (TestRequest.objects.all(),TestRequestSerializer),
        (TestReport.objects.all(),TestReportSerializer)
    ]
class TestReportView(MultipleModelAPIView):
    queryList = [
        (TestRequest.objects.order_by('-test_run_id')[:10],TestRequest2Serializer),
    ]

class ResultLogView(MultipleModelAPIView):
    queryList = [
        (TestRequest.objects.all(),TestRequest3Serializer),
    ]

class ResultView(MultipleModelAPIView):
    queryList = [
        (TestRequest.objects.all(),TestRequest4Serializer),
    ]
#-------------------------------------------------------------
from rest_framework.views import APIView
from rest_framework.response import Response
from serializers import ReportSerializer1
from rest_framework import status

class Report(APIView):
    serializer_class = ReportSerializer1
    def get(self, request, *args, **kw):
        #test_run = self.get_object(request.data)
        test_run = request.GET.get('test_run', None)
        response = Response(test_run, status=status.HTTP_200_OK)
        return response
 
