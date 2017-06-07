from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from employees.models import Employee

class Project(models.Model):
	"""stores all relevent data / meta about a project"""
	class Meta:
		verbose_name = _('project')

	WORK_TYPES = (
		('MECH', _('Mechanical')),
		('ELEC', _('Electronic')),
		('ASSM', _('Assembly'))
	)
	STATUS = (
		('INP', _('In-Progress')),
		('HLD', _('On Hold')),
		('CND', _('Cancelled')),
		('CMP', _('Completed'))
	)
	name = models.CharField(max_length=50, unique=True, verbose_name=_('project name')) #name or PN (need to improve)
	customer = models.ForeignKey('Customer', on_delete=models.PROTECT, verbose_name=_('customer'))
	work_type = models.CharField(max_length=4, choices=WORK_TYPES, verbose_name=_('project type'))
	status = models.CharField(max_length=3, choices=STATUS, verbose_name=_('status'))
	engineer = models.ManyToManyField(Employee, verbose_name=_('engineer'))
	estimated_hours = models.SmallIntegerField(null=True, verbose_name=_('estimated hours'))

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('projects.dashboard', args=[str(self.id)])

class Milestone(models.Model):
	"""stores milestones defined at the start of a project"""
	class Meta:
		ordering = ['deadline']
		verbose_name = _('milestone')
		
	project = models.ForeignKey(Project, on_delete=models.PROTECT, verbose_name=_('project'))
	description = models.CharField(max_length=50, verbose_name=_('milestone'))
	deadline = models.DateField(verbose_name=_('deadline'))
	completion_date = models.DateField(null=True, verbose_name=_('completion date'))
	gate_checklist = models.ForeignKey() 
		
	def __str__(self):
		return self.project.name + ' - ' + self.description

class Update(models.Model):
	"""stores project updates and meta"""
	class Meta:
		ordering = ['-mod_date']
		verbose_name = _('update')

	STAGES = (
		('WCUST', _('Waiting for Customer Response')), 
		('MKDFM', _('Creating DFM')),
		('TLDSN', _('Tooling Design')),
		('TLBLD', _('Tooling Build')),
		('TLTST', _('Tooling Testing')),
		('TLMOD', _('Tooling Modification')),
		('MKSMP', _('Creating Samples')),
		('IMSMP', _('Improving Samples')),
		('MK_WI', _('Creating WI')),
		('MKBOM', _('Creating BOM')),
		('MKECO', _('Creating ECO')),
		('PRVAL', _('Process Validation')),
		('PLTRN', _('Pilot Run')),
		('TFBLD', _('Building Test Fixture')),
	)
	project = models.ForeignKey(Project, on_delete=models.PROTECT, verbose_name=_('project')) # filled automatically
	stage = models.CharField(max_length=5, choices=STAGES, verbose_name=_('stage'))
	action_required = models.TextField(verbose_name=_('action required')) # this is are free text b/c too many combinations otherwise
	estimated_hours = models.SmallIntegerField(verbose_name=_('estimated hours'))
	mod_date = models.DateTimeField(auto_now_add=True, verbose_name=_('date'))
	mod_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_('user')) # some finesse required to set this

	def __str__(self):
		return self.project.name + ' - ' + self.mod_date.strftime('%Y/%m/%d')

class Customer(models.Model):
	"""stores info regarding customers [only name needed right now]"""
	name = models.CharField(max_length=50, unique=True, verbose_name=_('customer'))

	class Meta:
		verbose_name = _('customer')
	
	def __str__(self):
		return self.name