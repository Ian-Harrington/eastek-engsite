from django import forms
from django.core.exceptions import ValidationError
#from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _

from .models import Employee


class FilterListForm(forms.Form):
	"""handles sorting in the list view"""
	position = forms.ChoiceField(required=False, choices=(('',''),) + Employee.POSITIONS, label=_('Position')) # label needs work
	team = forms.ChoiceField(required=False, choices=(('',''),) + Employee.TEAMS, label=_('Team'))
	leader = forms.ModelChoiceField(required=False, queryset=Employee.objects.filter(is_leader=True), empty_label='',label=_('Leader')) # ModelChoiceField? - NO (okay now I wish i knew why)
	ret = forms.BooleanField(required=False, label=_('Retired'))

class IndividualForm(forms.ModelForm):
	"""handles displaying detail view info"""
	leader = forms.ModelChoiceField(queryset=Employee.objects.filter(is_leader=True), validators=[Employee.validate_leader], empty_label='', label=_('Leader'))
	# true if a user account is to be created for the employee (unbound), or there is already an account (bound)user_acc = forms.BooleanField(required=False, label='User account')
	email = forms.EmailField(validators=[Employee.validate_email], label=_('Email')) # make sure other validators remain
	emp_id = forms.CharField(min_length=4, max_length=5, validators=[Employee.validate_emp_id], label=_('Employee ID'))

	class Meta:
		model = Employee
		fields = ['emp_id', 'name', 'english_name', 'position', 'is_active', 'is_leader', 
			'team', 'leader', 'email', 'join_date', 'ret_date']
	
	def clean(self):
		super(IndividualForm, self).clean()
		if not self.cleaned_data['is_active'] and self.cleaned_data['ret_date'] == None:
			self.add_error(self.ret_date, ValidationError(_('Retired employees must have a retire date'))) # add to retire date
		if self.cleaned_data['ret_date'] != None and self.cleaned_data['is_active']:
			self.add_error(self.is_active, ValidationError(_('Employees with a retire date must be marked as retired'))) # add to is_active
		if self.cleaned_data['is_leader'] and self.cleaned_data['leader'].emp_id != self.cleaned_data['emp_id']:
			self.add_error('leader', ValidationError(_('A team leader must be their own team leader')))

	def clean_email(self):
		return self.cleaned_data['email'].lower()