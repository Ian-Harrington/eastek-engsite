from datetime import timedelta, date as pydate

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Overtime
from employees.models import Employee
from projects.models import Project, Defaults

class AddOvertime(forms.ModelForm):
	"""form for employees to use to add overtime"""
	def validate_date(date):
		if date < pydate.today():
			raise ValidationError(_('Cannot submit for overtime in the past'))
		elif date - pydate.today() > timedelta(days=1):
			raise ValidationError(_('Cannot submit for overtime more than 1 day in advance'))

	date = forms.DateField(validators=[validate_date], label=_('Date'))
	request_hours = forms.DecimalField(validators=[Overtime.validate_hours], max_digits=3, decimal_places=1, label=_('Request hours'), widget=forms.TextInput(attrs={'type':'number', 'step':'0.5'}))
	reason = forms.ChoiceField(choices=[('','---------')]+[(str(x[1]),x[1]) for x in Defaults.WORK_REASON])

	class Meta:
		model = Overtime
		fields = ['date', 'time', 'request_hours', 'project', 'reason']


class DatePicker(forms.Form):
	"""form to pick the date for overtime retrieval"""
	years = [x for x in range(2017, pydate.today().year+1)] # 2017 to current year
	date = forms.DateField(widget=forms.SelectDateWidget(years=years, empty_label=None), initial=pydate.today(), label=_('Date')) 
	# calendar widget? default to today?


class OvertimeFilter(forms.Form):
	"""docstring for OvertimeFilter"""
	years = [x for x in range(2017, pydate.today().year+1)] # 2017 to current year
	date = forms.DateField(required=False, widget=forms.SelectDateWidget(years=years, empty_label=''), label=_('Date'))
	emp = forms.ModelChoiceField(required=False, queryset=Employee.objects.all(), empty_label='', label=_('Employee'))
	project = forms.ModelChoiceField(required=False, queryset=Project.objects.filter(status='INP'), empty_label='', label=_('Project'))

class ActualHoursForm(forms.Form):
	"""form to input actual overtime hours worked"""
	actual_hours = forms.DecimalField(validators=[Overtime.validate_hours], max_digits=3, decimal_places=1, label=_('Request hours'), widget=forms.TextInput(attrs={'type':'number','step':'0.5'}))
	overtime_id = forms.IntegerField(min_value=0, max_value=Overtime.objects.count())
	