# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets')

#----------------------------TestRequest ------------------------
from snippets.models import TestRequest,Project



class ProjectSerializer(serializers.ModelSerializer):
   class Meta:
        model = Project
        fields = ('id','name',)


class TestRequestSerializer(serializers.ModelSerializer):
    #highlight = serializers.HyperlinkedIdentityField(view_name='testrequest-highlight', format='html')
    class Meta:
        model = TestRequest
        fields = ('url','id','user', 'project', 'test_suit_id', 'test_file')


