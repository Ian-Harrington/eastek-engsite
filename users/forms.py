from django.contrib.auth import password_validation
from django.utils.translation import ugettext_lazy as _
from django import forms

from .models import User
from projects.models import Project

class PasswordForm(forms.Form):
	"""docstring for PasswordForm"""
	BAD_PASSWORDS = ['password', '12345678', '88888888', 'abcdefgh', '1234.abcd']

	password1 = forms.CharField(min_length=8, widget=forms.PasswordInput, label=_('Password'))
	password2 = forms.CharField(min_length=8, widget=forms.PasswordInput, label=_('Confirm password'))

	def __init__(self, user, *args, **kwargs):
		self.user = user
		super(PasswordForm, self).__init__(*args, **kwargs)

	def clean(self):
		super(PasswordForm, self).clean()
		try:
			both_filled = self.cleaned_data['password1'] and self.cleaned_data['password2']
		except KeyError:
			raise forms.ValidationError(_('Must enter password in both fields'))
		if self.cleaned_data['password1'] != self.cleaned_data['password2']:
			self.add_error('password2', forms.ValidationError(_('Passwords must match')))
		return self.cleaned_data

	def clean_password1(self):
		try:
			new_pwd = self.cleaned_data['password1']
		except AttributeError:
			raise forms.ValidationError()
		password_validation.validate_password(new_pwd, self.user)
		for pwd in self.BAD_PASSWORDS:
			if new_pwd == pwd:
				raise forms.ValidationError(_('Password is too simple'))
		return new_pwd

class LinkForm(forms.Form):
	"""docstring for LinkForm"""
	link = forms.ModelChoiceField(queryset=Project.objects.filter(status='INP'), label=_('project link'), empty_label='')
	link_text = forms.CharField(max_length=17, required=False, label=_('link name'))
	
	def clean_link_text(self):
		if self.cleaned_data['link_text'] == '':
			return self.cleaned_data['link'].name[:17]
		return self.cleaned_data['link_text']

Link3Formset = forms.formset_factory(LinkForm, extra=3, max_num=3)