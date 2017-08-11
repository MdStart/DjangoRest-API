# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import generics
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnly1 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers



# class SnippetList(generics.ListCreateAPIView):
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer




# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer



#----------------------------------------
# @api_view
# def api_root(request, format=None):
#     return Response({
#         'users':reverse('user-list', request=request, format=format),
#         'snippets':reverse('snippet-list', request=request, format=format)
#         })


# class SnippetHighlight(generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     renderer_class = (renderers.StaticHTMLRenderer,)

#     def get(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)


from rest_framework import viewsets
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides 'list' and 'detail' actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


from rest_framework.decorators import detail_route

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list' and 'create', 'retrieve',
    'update' and 'destroy' actions.

    Additionally we also provide an extra 'highlight' action.
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

#----------------TestRequest -----------------------------

from snippets.models import TestRequest, Project
from snippets.serializers import TestRequestSerializer, ProjectSerializer
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


#--------------------------------------------------------------------------

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.reverse import reverse


# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'testrequests': reverse('testrequest-list', request=request, format=format)
#     })


# from rest_framework import renderers
# from rest_framework.response import Response

# class TestRequestHighlight(generics.GenericAPIView):
#     queryset = TestRequest.objects.all()
#     renderer_classes = (renderers.StaticHTMLRenderer,)

#     def get(self, request, *args, **kwargs):
#         testrequest = self.get_object()
#         return Response(testrequest.highlighted)