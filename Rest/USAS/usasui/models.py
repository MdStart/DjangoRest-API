
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User as superuser
from django.db import models

from django.core.files.storage import FileSystemStorage
import uuid


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=12)

    def __str__(self):
        return self.name

class Project(models.Model):
    user = models.ForeignKey(superuser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,unique=True,null=True, blank=True)

    def __str__(self):
        return self.name

def get_test_id():
    test_id = str(uuid.uuid4())[:11].replace('-', '').lower()
    #test_id = '9f16a22615'
    try:
        id_exists = TestRequest.objects.get(test_run_id=test_id)
        get_test_id()
    except:
        return test_id

class TestRequest(models.Model):
    WAITING = 'w'
    TESTING = 't'
    COMPLETED = 'c'
    ERROR = 'e'
    STATUS_CHOICES = (
        (WAITING, "Waiting"),
        (TESTING, "Testing"),
        (COMPLETED,"Completed"),
        (ERROR,"Error"),
    )

    test_run_id = models.CharField(max_length=50,default=get_test_id)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    execution = models.DateTimeField(blank=True,null=True)
    user = models.ForeignKey(superuser)
    project = models.ForeignKey(Project)
    test_suit_id = models.CharField(max_length=50)
    test_file = models.FileField()
    log_path = models.CharField(max_length=200,blank=True,null=True)
    status = models.CharField(choices=STATUS_CHOICES,max_length=10, default=WAITING)
    result = models.CharField(max_length=30,blank=True,null=True)
    envt = models.CharField(max_length=30,blank=True,null=True)

    def __str__(self):
        return self.test_run_id+"----> "+str(self.user)+ " ----> "+self.status


#--------------------------------------------------------------------------------------


class TestSuit(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TestCase(models.Model):
    project = models.ForeignKey(Project)
    testcase_id = models.CharField(max_length=20, null=True, blank=True)
    test_suit = models.ForeignKey(TestSuit)

    def __str__(self):
        return self.test_suit.name

class TestRun(models.Model):
    # PASS = 'p'
    # FAIL = 'f'
    # NORUN = 'n'

    # RESULT_CHOICES = (
    #     (PASS, "Pass"),
    #     (FAIL, "Fail"),
    #     (NORUN,"NoRun"),
    #     )
    # result = models.CharField(choices=RESULT_CHOICES,max_length=10)
    test_run_name = models.CharField(max_length=100)
    project = models.ForeignKey(Project)
    test_suit_name = models.ForeignKey(TestSuit)
    test_case = models.ManyToManyField(TestCase)
    test_request = models.ForeignKey(TestRequest, null=True, blank=True)
    
    result = models.CharField(max_length=20)

    def __str__(self):
        return self.test_run_name

class TestReport(models.Model):
    testrequest = models.ForeignKey(TestRequest)
    # name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name
