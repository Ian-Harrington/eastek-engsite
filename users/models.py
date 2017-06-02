from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from projects.models import Project

class User(AbstractUser):
	"""model for site user, handles authentication & permissions"""
	projlink1 = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('link 1'), related_name='user1')
	projlink2 = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('link 2'), related_name='user2')
	projlink3 = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('link 3'), related_name='user3')
	link1txt = models.CharField(blank=True, max_length=17, verbose_name=_('link 1 text'))
	link2txt = models.CharField(blank=True, max_length=17, verbose_name=_('link 2 text'))
	link3txt = models.CharField(blank=True, max_length=17, verbose_name=_('link 3 text'))

	def __str__(self):
		return self.username
