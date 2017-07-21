from datetime import date as Date

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.utils.translation import ugettext_lazy as _

from EngSite.utils.reportgen import generate_overtime_report
from projects.models import Project
from .models import Overtime
from .forms import AddOvertime, DatePicker, OvertimeFilter, ActualHoursForm

@permission_required('overtime.add_overtime', raise_exception=True)
def add_overtime(request):
	context = {}
	if request.method == 'POST':
		ot = Overtime.objects.filter(date=request.POST.get('date')).filter(emp=request.user.employee)
		if ot.count() == 0: # a lot of extra work just for a small notification (necessary?)
			form = AddOvertime(request.POST)
			form.instance.emp = request.user.employee # need way to test and catch users w/o attached employees 
			context['notice'] = _('Overtime recorded successfully')
		else:
			form = AddOvertime(request.POST, instance=ot[0])
			context['notice'] = _('Previously submitted overtime has been overwritten')

		if form.is_valid():
			form.save()
		else:
			context['notice'] = _('Not saved. Invalid data.')
	else:
		form = AddOvertime(initial={'date': Date.today()})
	context['form'] = form
	return render(request, 'overtime/add.html', context)


@permission_required('overtime.view_overtime', raise_exception=True)
def overtimerequest(request):
	context = {}
	if request.method == 'POST':
		# makes the pdf with the sent info
		form = DatePicker(request.POST)
		if form.is_valid():
			date = form.cleaned_data['date']
			ot = Overtime.objects.filter(date=date)
			if ot.exists():
				response = HttpResponse(generate_overtime_report(overtime=ot), content_type='application/vnd.ms-excel')
				response['Content-Disposition'] = 'attachment; filename="' + str(date) + '_Overtime.xlsx"'
				return response
			else:
				context['notice'] = _('No overtime recorded on selected date')
		else:
			context['notice'] = _('Invalid date provided')
	# user requests the date selection page
	form = DatePicker()
	context['dateform'] = form
	return render(request, 'overtime/request.html', context)


class OvertimeListView(PermissionRequiredMixin, ListView):
	"""handles the overtime list view"""
	raise_exception = True
	permission_required = 'overtime.view_overtime'
	template_name = 'overtime/list.html'
	model = Overtime
	paginate_by = 50

	def get_queryset(self, **kwargs):
		# isn't executed every time 
		qs = super(OvertimeListView, self).get_queryset(**kwargs)
		if self.request.method == 'GET': 
			if self.request.GET.get('emp') != '' and self.request.GET.get('emp') != None:
				qs = qs.filter(emp=self.request.GET.get('emp'))
			if self.request.GET.get('date_day') != None and self.request.GET.get('date_month') != None and self.request.GET.get('date_year') != None:
				try:
					y = int(self.request.GET.get('date_year'))
					m = int(self.request.GET.get('date_month'))
					d = int(self.request.GET.get('date_day'))
					qs = qs.filter(date=Date(y,m,d))
				except ValueError:
					pass
			if self.request.GET.get('project') != '':
				qs = qs.filter(project=self.request.GET.get('project'))
		return qs

	def get_context_data(self, **kwargs):
		# rarely is executed
		context = super(OvertimeListView, self).get_context_data(**kwargs)
		context['form'] = OvertimeFilter()
		return context

@login_required
@permission_required('overtime.view_overtime', raise_exception=True)
def overtime_list(request, page):
	ot = Overtime.objects.all()
	form = OvertimeFilter()
	if request.GET:
		y = int(request.GET.get('date_year'))
		m = int(request.GET.get('date_month'))
		d = int(request.GET.get('date_day'))
		filters = {
			'emp': request.GET.get('emp'),
			'project': request.GET.get('project'),
		}
		if filters['emp'] != '':
			ot = ot.filter(emp=filters['emp'])
		#if request.GET.get('date_day') != None and request.GET.get('date_month') != None and request.GET.get('date_year') != None:
		if d > 0 and m > 0 and y > 2000:
			ot = ot.filter(date=Date(y,m,d))
			filters['date_year'] = y
			filters['date_month'] = m
			filters['date_day'] = d
		if filters['project'] != '':
			ot = ot.filter(project=filters['project'])
		form = OvertimeFilter(filters)
	paginator = Paginator(ot, 50)
	context = {'form': form, 'page_obj': paginator.page(page), 'overtime': Overtime, 'AH_form':ActualHoursForm()}
	return render(request, 'overtime/list.html', context)

@require_POST
@permission_required('overtime.change_overtime', raise_exception=True)
def add_actual_hours(request, page):
	AH_form = ActualHoursForm(request.POST)
	if AH_form.is_valid():
		overtime = get_object_or_404(Overtime, pk=AH_form.cleaned_data['overtime_id'])
		assert overtime.id == AH_form.cleaned_data['overtime_id']
		overtime.actual_hours = AH_form.cleaned_data['actual_hours']
		overtime.save()
	return HttpResponseRedirect('/overtime/list/' + page)