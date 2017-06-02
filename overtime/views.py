from datetime import date as Date

from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from projects.models import Project
from .models import Overtime
from .forms import AddOvertime, DatePicker, OvertimeFilter
from .reportgen import generate_overtime_report #genOTpdf, OTlines

@login_required
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
		form = AddOvertime()
	context['form'] = form
	return render(request, 'overtime/add.html', context)

@login_required
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
				# making the pdf (this is going to be a shitload of work)
				# a temporary work around could be to export as csv (can run macro on?)
				"""
				response = HttpResponse(content_type='application/pdf')
				response['Content-Disposition'] = 'attachment; filename="' + request.POST.get('date') + '_Overtime.pdf"'
				response.write(genOTpdf(ot)) # might want/need this to be a tuple or list rather than qs 
				return response
				"""
				response = HttpResponse(generate_overtime_report(overtime=ot), content_type='application/vnd.ms-excel')
				response['Content-Disposition'] = 'attachment; filename="' + str(date) + '_Overtime.xlsx"'
				"""
				# CSV method
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="' + str(date) + '_Overtime.csv"'
				wtr = csv.writer(response)
				for ln in OTlines(ot):
					wtr.writerow(ln)
				"""
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
		qs = super(OvertimeListView, self).get_queryset(**kwargs)
		assert isinstance(qs, QuerySet)
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
		return qs

	def get_context_data(self, **kwargs):
		context = super(OvertimeListView, self).get_context_data(**kwargs)
		context['form'] = OvertimeFilter()
		return context

'''
# I don't like class based views, too confusing
class AddProjectView(PermissionRequiredMixin, CreateView):
	"""handles the add project view for the stand-in project model"""
	raise_exception = True
	permission_required = 'overtime.add_project'
	template_name = 'overtime/addproject.html'
	model = Project
	fields = ['name', 'customer']
	success_url = reverse_lazy('overtime:listproject')

class EditProjectView(PermissionRequiredMixin, UpdateView):
	"""handles the add project view for the stand-in project model"""
	raise_exception = True
	permission_required = 'overtime.edit_project'
	template_name = 'overtime/editproject.html'
	model = Project
	fields = ['name', 'customer']

class ListProjectView(PermissionRequiredMixin, ListView):
	raise_exception = True
	permission_required = 'overtime.add_project'
	template_name = 'overtime/listproject.html'
	model = Project
'''