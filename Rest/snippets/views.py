# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

#----------------TestRequest -----------------------------

from snippets.models import TestRequest, Project, TestCase
from snippets.serializers import TestRequestSerializer, ProjectSerializer, TestCaseSerializer
from rest_framework import generics
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

