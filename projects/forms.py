from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from users.models import User
from employees.models import Employee
from . import models

class ProjectFilter(forms.Form):
	"""docstring for ProjectFilter"""
	customer = forms.ModelChoiceField(required=False, queryset=models.Customer.objects.all(), empty_label='', label=_('Customer'))
	work_type = forms.ChoiceField(required=False, choices=(('',''),)+models.Project.WORK_TYPES, label=_('Project type'))
	status = forms.ChoiceField(required=False, choices=(('',''),)+models.Project.STATUS, label=_('Status'))
	engineer = forms.ModelChoiceField(required=False, queryset=Employee.objects.filter(is_active=True), empty_label='', label=_('Engineer'))


class ProjectStatusForm(forms.Form):
	"""docstring for ProjectStatusForm"""
	status = forms.ChoiceField(choices=models.Project.STATUS, label=_('Status'))


class CheckForm(forms.Form):
	"""docstring for CheckForm"""
	chk = forms.BooleanField(required=False)

CheckFormset = forms.formset_factory(CheckForm)
		

class ProjectForm(forms.ModelForm):
	"""docstring for ProjectForm"""
	class Meta:
		model = models.Project
		fields = ['name', 'customer', 'work_type', 'status', 'engineer']
		# labels not needed to be set since they are drawn from the model verbose_name 


class MilestoneForm(forms.ModelForm):
	"""docstring for MilestoneForm"""
	remarks = forms.CharField(widget=forms.Textarea(attrs={'rows':2}), required=False, label=_('remarks'))
	description = forms.CharField(widget=forms.TextInput(attrs={'size':30}), label=_('milestone'))
	deadline = forms.DateField(widget=forms.TextInput(attrs={'size':12}), label=_('deadline'))

	class Meta:
		model = models.Milestone
		fields = ['description', 'deadline', 'remarks']
'''
	def  __init__(self, **kwargs):
		super(MilestoneForm, self).__init__(**kwargs)
		self.fields['description'].widget.attrs['readonly'] = 'true'
'''

class UpdateForm(forms.ModelForm):
	"""docstring for UpdateForm"""
	project = forms.CharField(widget=forms.HiddenInput())
	mod_user = forms.ModelChoiceField(queryset=get_user_model().objects.all(), to_field_name='id', widget=forms.HiddenInput())
	estimated_hours = forms.IntegerField(max_value=500, min_value=0, label=_('Estimated hours'))

	class Meta:
		model = models.Update
		fields =['project', 'stage', 'action_required', 'estimated_hours', 'mod_user']
		widgets = {'action_required': forms.Textarea(attrs={'rows': 4})}

	def clean_project(self):
		try:
			val = self.cleaned_data['project']
		except AttributeError:
			raise forms.ValidationError()
		try:
			instance = models.Project.objects.get(id=val)
		except Project.DoesNotExist:
			raise forms.ValidationError(_('Associated project not found'))
		return instance

	def clean_mod_user(self):
		try:
			val = self.cleaned_data['mod_user']
		except AttributeError:
			raise forms.ValidationError()
		User = get_user_model()
		try:
			instance = User.objects.get(username=val)
		except User.DoesNotExist:
			raise forms.ValidationError(_('User instance not found'))
		return instance


class CustomerForm(forms.ModelForm):
	"""docstring for CustomerForm"""
	class Meta:
		model = models.Customer
		fields = ['name'] # may need to expand later


ChecklistFormset = forms.modelformset_factory(models.ChecklistItem, fields=['name', 'responsible', 'completed', 'remarks'])