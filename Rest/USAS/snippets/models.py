# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
#-------------------------------------------------------------------------------
from django.contrib.auth.models import User as superuser

import uuid

class Project(models.Model):
    user = models.ForeignKey('auth.User', related_name='project',on_delete=models.CASCADE, null=True)
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
    user = models.ForeignKey(superuser ,on_delete=models.CASCADE)
    project = models.ForeignKey(Project)
    test_suit_id = models.CharField(max_length=50)
    test_file = models.FileField()
    log_path = models.CharField(max_length=200,blank=True,null=True)
    highlighted = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES,max_length=10, default=WAITING)
    result = models.CharField(max_length=30,blank=True,null=True)
    #envt = models.CharField(max_length=30,blank=True,null=True)

    def __str__(self):
        return self.test_run_id+"----> "+str(self.user)+ " ----> "+self.status

