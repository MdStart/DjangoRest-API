
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.models import ModelMultipleChoiceField
from .models import TestRequest,Project,TestCase,TestRun

class TestRequestForm(ModelForm):
	class Meta:
		model = TestRequest
		exclude = ('test_run_id','start_time','end_time','result','test_suit_id','log_path','execution','envt')
		#fields = '__all__'
 
class ProjectForm(ModelForm):
	class Meta:
		model = Project
		fields = ('name',)

#-----------------------------------

class TestCaseForm(ModelForm):
	class Meta:
		model = TestCase
		fields = '__all__'

class TestRunForm(ModelForm):
	class Meta:
		model = TestRun
		# fields = '__all__'
		# exclude =('test_request')
		fields = ('test_run_name','project','test_case')

