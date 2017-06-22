from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from employees.models import Employee
from projects.models import Project


class Overtime(models.Model):
	"""model representing an occurance of overtime work"""
	class Meta:
		permissions = (('view_overtime', _('Can view overtime')),)
		ordering = ['-date']
		verbose_name=_('overtime')
		verbose_name_plural=_('overtime')


	# validate for hours fields (0 hrs < hours < 24 hrs & res = .5 hrs)
	def validate_hours(hours):
		if hours > 24:
			raise ValidationError(_('Overtime hours cannot exceed 24 hours for a given day'))
		elif hours < 0:
			raise ValidationError(_('Overtime hours must be greater than 0'))
		elif float(hours) % .5 != 0: # is this true?
			raise ValidationError(_('Overtime hours must be recorded to the half hour'))

	date = models.DateField(verbose_name=_('date'))
	time = models.TimeField(verbose_name=_('time'))
	request_hours = models.DecimalField(max_digits=3, decimal_places=1, validators=[validate_hours], verbose_name=_('request hours'))
	actual_hours = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, validators=[validate_hours], verbose_name=_('hours worked'))
	emp = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='overtime', verbose_name=_('employee'))
	project = models.ForeignKey(Project, on_delete=models.PROTECT, verbose_name=_('project')) #choice limiting done at the form level
	reason = models.CharField(max_length=120, verbose_name=_('reason'))

	def __str__(self):
		return self.emp.english_name + ' - ' + str(self.date)