# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from rest_framework import serializers
from USAS import settings

#----------------------------TestRequest ------------------------
from models import TestRequest,Project, TestCase, TestRun, TestReport



class ProjectSerializer(serializers.ModelSerializer):
   class Meta:
        model = Project
        fields = ('user','name',)


class TestRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestRequest
        fields = ('url','project','test_suit_id','test_file')

class TestRequest3Serializer(serializers.ModelSerializer):
    class Meta:
        model = TestRequest
        fields = ('test_run_id','log_path')

class TestRequest4Serializer(serializers.ModelSerializer):
    class Meta:
        model = TestRequest
        fields = ('test_run_id','result')

class TestRequest2Serializer(serializers.ModelSerializer):
    #highlight = serializers.HyperlinkedIdentityField(view_name='testrequest-highlight', format='html')
    #highlight = serializers.HyperlinkedIdentityField(view_name='usasui:testview-detail', format='html')
    '''log_path_url = serializers.SerializerMethodField('get_log_path_url')
    def get_log_path_url(self, obj):
        return '%s%s' % (settings.MEDIA_URL, obj.log_path)'''
    class Meta:
        model = TestRequest
        fields = ('test_run_id','user', 'project','test_suit_id','envt','status', 'result','log_path','test_file')
        #extra_kwargs = {
        #    'url': {'view_name': 'usasui:testview-detail'}
        #}


class TestCaseSerializer(serializers.ModelSerializer):
    #highlight = serializers.HyperlinkedIdentityField(view_name='testrequest-highlight', format='html')
    class Meta:
        model = TestCase
        fields = ('project', 'testcase_id', 'test_suit')

class TestRunSerializer(serializers.ModelSerializer):
   class Meta:
        model = TestRun
        fields = ('test_run_name','project','test_suit_name','test_case','test_request')

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestRequest
        fields = ('__all__')

class TestReportSerializer(serializers.ModelSerializer):
    #report = TestRequestSerializer(read_only=True)
    class Meta:
        model = TestReport
        fields = ('id','testrequest')

class ReportSerializer1(serializers.Serializer):
    test_run = serializers.CharField(max_length=50)
