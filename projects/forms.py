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
	engineer = forms.ModelChoiceField(required=False, queryset=Employee.objects.filter(is_active=True).exclude(team='SUPP'), empty_label='---------', label=_('Engineer'))
	class Meta:
		model = models.Project
		fields = ['name', 'customer', 'eastek_pn', 'cust_pn', 'engineer', 'work_type', 'status'] #lead_eng

class PartNumForm(forms.Form):
	partnum = forms.CharField(max_length=50, min_length=5, strip=True, label=_('part number'))


class MilestoneForm(forms.ModelForm):
	"""docstring for MilestoneForm"""
	deadline = forms.DateField(widget=forms.DateInput(attrs={'class':'deadline-input'}), label=_('deadline'))
	class Meta:
		model = models.Milestone
		fields = ['description', 'deadline']

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


class ChecklistForm(forms.ModelForm):
	"""docstring for ChecklistForm"""
	def validate_completed(value):
		if value == 'False':
			raise forms.ValidationError(_('Item must be completed or not applicable'))

	completed = forms.ChoiceField(required=False, choices=models.ChecklistItem.COMP_CHOICE, validators=[validate_completed], label=_('Completed'))

	class Meta:
		model = models.ChecklistItem
		fields = ['name', 'responsible', 'completed', 'remarks']


ChecklistFormset = forms.formset_factory(ChecklistForm)