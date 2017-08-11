# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)


    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)

        
    class Meta:
        ordering = ('created',)


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

