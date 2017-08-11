# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from rest_framework import serializers

#----------------------------TestRequest ------------------------
from snippets.models import TestRequest,Project, TestCase, TestRun, TestReport



class ProjectSerializer(serializers.ModelSerializer):
   class Meta:
        model = Project
        fields = ('id','name',)


class TestRequestSerializer(serializers.ModelSerializer):
    #highlight = serializers.HyperlinkedIdentityField(view_name='testrequest-highlight', format='html')
    class Meta:
        model = TestRequest
        fields = ('url','id','user', 'project', 'test_suit_id', 'test_file')

class TestCaseSerializer(serializers.ModelSerializer):
    #highlight = serializers.HyperlinkedIdentityField(view_name='testrequest-highlight', format='html')
    class Meta:
        model = TestCase
        fields = ('project', 'testcase_id', 'test_suit')

class TestRunDownload(ModelSerializer):
    class Meta:
        model = TestRun
        fields = ('test_run_id',)

class TestReport(ModelSerializer):
    class Meta:
        model = TestReport
        fields = ('testrequest', 'name')