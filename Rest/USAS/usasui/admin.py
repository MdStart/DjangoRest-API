
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin


# Register your models here.
from .models import User,Project,TestRequest,TestSuit,TestCase,TestRun

class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User

    list_display = ('name','email','phone')


class TestRequestAdmin(admin.ModelAdmin):
    class Meta:
        model = TestRequest

    list_display = ('test_run_id','user','project','test_suit_id','status','created','execution')


class TestRunAdmin(admin.ModelAdmin):
	class Meta:
		model = TestRun
	list_display = ('test_request','result')	


admin.site.register(User,UserAdmin)
admin.site.register(Project)
admin.site.register(TestRequest,TestRequestAdmin)
#--------------------------------------------------

admin.site.register(TestSuit)
admin.site.register(TestCase)
admin.site.register(TestRun,TestRunAdmin)


