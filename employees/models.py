import re

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _


class Employee(models.Model):
	"""contains the data from EmployeeInfo table"""
	class Meta:
		ordering = ['emp_id']
		verbose_name = _('Employee')


	EASTEK_EMAIL_REGEX = r'^[a-z]+\.[a-z]+@(?:eastek)(?:-intl|international)\.com$'
	ASSISTANT_ENG = 'AEN'
	ENGINEER = 'ENG'
	SENIOR_ENG = 'SEN'
	LEADER = 'LDR'
	CLERK = 'CLK'
	TOOLING_ENG = 'TEN'
	POSITIONS = (
		(ASSISTANT_ENG, _('Assistant Engineer')),
		(ENGINEER, _('Engineer')),
		(SENIOR_ENG, _('Senior Engineer')),
		(LEADER, _('Engineer Leader')),
		(CLERK, _('Clerk')),
		(TOOLING_ENG, _('Tooling Engineer')),
	)
	MECHANICAL = 'MECH'
	ELECTRONIC = 'ELEC'
	SUPPORT = 'SUPP'
	TOOLING = 'TOOL'
	TEAMS = (
		(MECHANICAL, _('Mechanical')),
		(ELECTRONIC, _('Electronics')),
		(SUPPORT, _('Support')),
		(TOOLING, _('Tooling')),
	)

	# Need this to be CharField b/c emp_ids start w/ 0
	emp_id = models.CharField(max_length = 5, primary_key=True, verbose_name=_('employee ID'))
	name = models.CharField(max_length=25, verbose_name=_('name'))
	english_name = models.CharField(max_length=40, verbose_name=_('english name'))
	position = models.CharField(max_length=3, choices=POSITIONS, verbose_name=_('position')) # will need translating fix 
	is_active = models.BooleanField(default=True, verbose_name=_('employed'))
	is_leader = models.BooleanField(default=False, verbose_name=_('is leader')) # need this because support leader isn't LDR
	team = models.CharField(max_length=4, choices=TEAMS, verbose_name=_('team'))
	leader = models.ForeignKey('self', on_delete=models.PROTECT, limit_choices_to={'is_leader': True}, verbose_name=_('leader'))
	email = models.EmailField(unique=True, verbose_name=_('email'))
	join_date = models.DateField(verbose_name=_('join date'))
	ret_date = models.DateField(blank=True, null=True, verbose_name=_('retire date'))
	account = models.OneToOneField(settings.AUTH_USER_MODEL, null=True,
		on_delete=models.SET_NULL, blank=True, verbose_name=_('user account')) 

	def __str__(self):
		return self.english_name

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('employees.detail', args=[self.emp_id])

	def get_leaders(): # don't think this is used
		leaders = []
		for ldr in Employee.objects.filter(is_leader=True):
			leaders.append((ldr.emp_id, ldr.english_name))
		return leaders

	def validate_email(email): 
		#regex for eastek email & no duplicates
		email.lower()
		if re.match(Employee.EASTEK_EMAIL_REGEX, email) == None: # is None ?
			raise ValidationError(_('Email must be a valid @eastek-intl.com or @eastekinternational.com email address'))

	def validate_leader(leader):
		#ensure leader has is_leader field active, shouldn't be triggered b/c ModelChoiceField
		if not leader.is_leader:
			raise ValidationError(_("Employee selected for leader must have 'Is leader' attribute"))

	def validate_emp_id(emp_id):
		if re.match(r'^[0-9]{4,5}$', emp_id) == None:
			raise ValidationError(_('Employee ID must be numerals only and 4-5 digits long'))
	
	def generate_user(self, supress=True):
		# check if custom user is implemented (quit if not?)
		if not self.has_user(): 
			username = self.email.split('@')[0]
			password = self.email.split('.')[0].lower() + '.' + self.emp_id
			User = get_user_model()
			if not User.objects.filter(username=username).exists():
				user = User.objects.create_user(username=username, email=self.email, password=password)
				assert isinstance(user, User), user
				user.groups.add(Group.objects.get(name='default'))
				if self.team == 'SUPP':
					user.groups.add(Group.objects.get(name='manager'))
				if not self.is_active:
					user.is_active = False
					user.save()
				self.account = user
				self.save()
				return user
			elif not supress:
				return False # user already exists
		elif not supress:
			return False # employee has account

	# returns the status of the presence of an associated user account
	def has_user(self):
		User = get_user_model()
		return isinstance(self.account, User)

	# if this user has been marked as retired, archive the associated account
	def archive_account(self):
		if not self.is_active and self.has_user():
			self.account.is_active = False
			self.account.save()
