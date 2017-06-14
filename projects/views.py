from datetime import date

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import formset_factory

from EngSite.utils.utils import choice_lookup
from employees.models import Employee
from . import models, forms


@login_required
@permission_required('projects.change_project', raise_exception=True)
def project_page(request, pid):
	project = get_object_or_404(models.Project, pk=pid)
	milestones = models.Milestone.objects.filter(project=project.id)
	updates = models.Update.objects.filter(project=project.id)
	form = forms.ProjectStatusForm(initial={'status': project.status})
	init = {'form-TOTAL_FORMS':str(milestones.count()),
			'form-INITIAL_FORMS':'0',
			'form-MIN_NUM_FORMS':'',
			'form-MAX_NUM_FORMS':''}
	for i in range(milestones.count()):
		init['form-'+str(i)+'-chk'] = milestones[i].is_complete
	formset = forms.CheckFormset(init)
	ms_fs = list(zip(milestones, formset))
	if updates.exists():
		status = updates[0]
	else:
		status = None
	context = {'project': project, 
				'projstatus': form, 
				'milestones': milestones, 
				'status': status,
				'ms_fs': ms_fs,
				'formset': formset,
				'work_opts': models.Project.WORK_TYPES,
				'status_opts': models.Project.STATUS,
				'stage_opts': models.Update.STAGES}
	return render(request, 'projects/project.html', context)


@require_POST
@permission_required('projects.change_project', raise_exception=True)
def change_project_status(request, pid):
	try:
		project = models.Project.objects.get(pk=pid)
	except models.Project.DoesNotExist:
		return HttpResponseRedirect('/projects/' + pid)
	form = forms.ProjectStatusForm(request.POST)
	if form.is_valid():
		project.status = form.cleaned_data['status']
		project.save()
	return HttpResponseRedirect('/projects/' + pid)


@require_POST
@permission_required('projects.change_project', raise_exception=True)
def add_self_to_project(request, pid):
	try:
		project = models.Project.objects.get(pk=pid)
	except models.Project.DoesNotExist:
		return HttpResponseRedirect('/projects/' + pid)
	try:
		eng = request.user.employee
	except RelatedObjectDoesNotExist:
		return HttpResponseRedirect('/projects/' + pid)
	project.engineer.add(eng)
	return HttpResponseRedirect('/projects/' + pid)


@require_POST
@permission_required('projects.change_project', raise_exception=True)
def change_milestone_completion(request, pid):
	try:
		project = models.Project.objects.get(pk=pid)
	except models.Project.DoesNotExist:
		return HttpResponseRedirect('/projects/' + pid)
	formset = forms.CheckFormset(request.POST)
	if formset.is_valid():
		for i in range(project.milestone_set.all().count()): 
			ms = project.milestone_set.all()[i]
			try:
				ms.is_complete = formset[i].cleaned_data['chk']
			except KeyError:
				ms.is_complete = False
			ms.save()
	return HttpResponseRedirect('/projects/' + pid)


@login_required
@permission_required('projects.add_project', raise_exception=True)
def add_project(request):
	formset = formset_factory(forms.MilestoneForm, can_delete=True)
	default = {'form-TOTAL_FORMS':'5',
				'form-INITIAL_FORMS':'0',
				'form-MIN_NUM_FORMS':'',
				'form-MAX_NUM_FORMS':'',
				'form-0-description': 'Kickoff',
				'form-1-description': 'Tool Design',
				'form-2-description': 'Qualification',
				'form-3-description': 'Pilot Run',
				'form-4-description': 'First Production Run',}
	if request.method == 'POST':
		proj_form = forms.ProjectForm(request.POST)
		mstn_form = formset(request.POST)
		if proj_form.is_valid() and mstn_form.is_valid():
			proj_form.save()
			proj = models.Project.objects.get(name=proj_form.cleaned_data['name'])
			for frm in mstn_form:
				ms = frm.save(commit=False)
				ms.project = proj
				ms.save()
			return HttpResponseRedirect('/projects/' + str(proj.id))
	else:
		proj_form = forms.ProjectForm()
		mstn_form = formset(default)
	context = {'proj_form': proj_form, 'formset': mstn_form}
	return render(request, 'projects/add_project.html', context)


@login_required
@permission_required('projects.add_update', raise_exception=True)
def add_update(request, pid):
	if request.method == 'POST':
		form = forms.UpdateForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/projects/' + pid)
	else:
		init = {'project': pid, 'mod_user': request.user.id}
		form = forms.UpdateForm(initial=init)
	context = {'form': form, 'pid': pid}
	return render(request, 'projects/add_update.html', context)


class ProjectListView(PermissionRequiredMixin, ListView):
	raise_exception = True
	permission_required = 'projects.change_project' # not really accurate
	template_name = 'projects/project_list.html' 
	model = models.Project

	def get_queryset(self, **kwargs):
		qs = super(ProjectListView, self).get_queryset(**kwargs)
		#assert isinstance(qs, QuerySet)
		if self.request.GET: # not self.request.method == 'GET' b/c default filter
			if self.request.GET.get('customer'):
				qs = qs.filter(customer=self.request.GET.get('customer'))
			if self.request.GET.get('work_type'):
				qs = qs.filter(work_type=self.request.GET.get('work_type'))
			if self.request.GET.get('status'):
				qs = qs.filter(status=self.request.GET.get('status'))
			if self.request.GET.get('engineer'):
				qs = qs.filter(engineer=self.request.GET.get('engineer'))
		else:
			qs = qs.filter(status='INP') # default to only show in-progress
		return qs

	def get_context_data(self, **kwargs):
		context = super(ProjectListView, self).get_context_data(**kwargs)
		if self.request.GET:
			data = {
				'customer': self.request.GET.get('customer'), 
				'work_type': self.request.GET.get('work_type'), 
				'status': self.request.GET.get('status'), 
				'engineer': self.request.GET.get('engineer')}
			context['form'] = forms.ProjectFilter(data)
		else:
			context['form'] = forms.ProjectFilter(initial={'status':'INP'})
		context['work_opts'] = models.Project.WORK_TYPES
		context['status_opts'] = models.Project.STATUS
		return context


@login_required
@permission_required('projects.change_update', raise_exception=True)
def project_updates(request, pid):
	qs = models.Update.objects.filter(project=pid)
	context = {'updates': qs, 'stage_opts': models.Update.STAGES, 'project':models.Project.objects.get(pk=pid)}
	return render(request, 'projects/update_list.html', context)


class CustomerListView(PermissionRequiredMixin, ListView):
	raise_exception = True
	permission_required = 'projects.add_customer'
	template_name = 'projects/customer_list.html' 
	model = models.Customer
	queryset = models.Customer.objects.order_by('name')
	paginate_by = 50	

	def get_context_data(self, **kwargs):
		context = super(CustomerListView, self).get_context_data(**kwargs)
		context['form'] = forms.CustomerForm()
		return context


@require_POST
@permission_required('projects.add_customer', raise_exception=True)
def add_customer(request):
	form = forms.CustomerForm(request.POST)
	if form.is_valid():
		form.save()
	return HttpResponseRedirect('/projects/customers/')


@permission_required('projects.change_checklist', raise_exception=True)
def complete_checklist(request, pid, gate):
	if request.method == 'POST':
		formset = ChecklistFormset(request.POST)
		if formset.is_valid():
			items = formset.save(commit=False)
			for item in items:
				item.milestone = None # make this the real thing
				item.save()
			return HttpResponseRedirect('projects/'+pid)
	else:
		# where will the defaults be located?
		init = {
			'form-TOTAL_FORMS':'5', # may need to be dynamic
			'form-INITIAL_FORMS':'0',
			'form-MIN_NUM_FORMS':'',
			'form-MAX_NUM_FORMS':'',
		}
		checklist = GATE_LIST[gate-1]
		for i in range(len(checklist)):
			init['form-'+str(i)+'-name'] = checklist[i][0]
			init['form-'+str(i)+'-responsible'] = checklist[i][1]
			init['form-'+str(i)+'-completed'] = False
			init['form-'+str(i)+'-remarks'] = ''
			# don't know if the pre-existing remarks are supposed to be added or not
		formset = ChecklistFormset(init, queryset=models.ChecklistItem.objects.none())
	context = {'formset': formset}
	return render(request, 'projects/checklist.html', context)

# view for editing checklist defaults