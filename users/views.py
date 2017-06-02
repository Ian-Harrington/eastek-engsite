from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from users.forms import PasswordForm, Link3Formset

@login_required
def change_password(request):
	if request.method == 'POST':
		pwd_form = PasswordForm(request.user, request.POST)
		if pwd_form.is_valid():
			request.user.set_password(pwd_form.cleaned_data['password1'])
			request.user.save()
			notice = _('Password saved successfully')
		else:
			notice = _('Password not saved')
	else:
		notice = None
	pwd_form = PasswordForm(request.user) # shouldn't return a bound form
	context = {'form': pwd_form, 'notice': notice}
	return render(request, 'users/pwd_change.html', context)

@login_required
def set_home_projects(request):
	user = request.user
	if request.method == 'POST':
		formset = Link3Formset(request.POST)
		if formset[0].is_valid() or formset[1].is_valid() or formset[2].is_valid():
			if formset[0].is_valid():
				user.projlink1 = formset[0].cleaned_data['link']
				user.link1txt = formset[0].cleaned_data['link_text']
			if formset[1].is_valid():
				user.projlink2 = formset[1].cleaned_data['link']
				user.link2txt = formset[1].cleaned_data['link_text']
			if formset[2].is_valid():
				user.projlink3 = formset[2].cleaned_data['link']
				user.link3txt = formset[2].cleaned_data['link_text']
			user.save()
	else:
		data = {
			'form-TOTAL_FORMS':'3',
			'form-INITIAL_FORMS':'0',
			'form-MIN_NUM_FORMS':'',
			'form-MAX_NUM_FORMS':'',
			'form-0-link': user.projlink1,
			'form-0-link_text': user.link1txt,
			'form-1-link': user.projlink2,
			'form-1-link_text': user.link2txt,
			'form-2-link': user.projlink3,
			'form-2-link_text': user.link3txt,
		}
		formset = Link3Formset(data)
	context = {'formset': formset}
	return render(request, 'users/set_links.html', context)