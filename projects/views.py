from datetime import date

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import formset_factory

from EngSite.utils.utils import choice_lookup
from EngSite.utils.reportgen import generate_gate_checklist
from employees.models import Employee
from . import models, forms


@login_required
@permission_required('projects.change_project', raise_exception=True)
def project_page(request, pid):
	project = get_object_or_404(models.Project, pk=pid)
	milestones = models.Milestone.objects.filter(project=project.id)
	updates = models.Update.objects.filter(project=project.id)
	form = forms.ProjectStatusForm(initial={'status': project.status})
	if updates.exists():
		status = updates[0]
	else:
		status = None
	context = {'project': project, 
				'projstatus': form, 
				'milestones': milestones, 
				'status': status,
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
	formset = formset_factory(forms.MilestoneForm)
	default = {'form-TOTAL_FORMS':'5',
				'form-INITIAL_FORMS':'0',
				'form-MIN_NUM_FORMS':'',
				'form-MAX_NUM_FORMS':'',
				'form-0-description': GATE_LIST[0][0],
				'form-1-description': GATE_LIST[1][0],
				'form-2-description': GATE_LIST[2][0],
				'form-3-description': GATE_LIST[3][0],
				'form-4-description': GATE_LIST[4][0],}
	if request.method == 'POST':
		proj_form = forms.ProjectForm(request.POST)
		mstn_form = formset(request.POST)
		if proj_form.is_valid() and mstn_form.is_valid():
			proj = proj_form.save()
			for frm in mstn_form:
				ms = frm.save(commit=False)
				ms.project = proj
				ms.save()
			return HttpResponseRedirect('/projects/' + str(proj.id))
	else:
		proj_form = forms.ProjectForm(initial={'status':'INP'})
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
		formset = forms.ChecklistFormset(request.POST)
		if formset.is_valid():
			milestone = models.Milestone.objects.filter(project=pid).get(description=GATE_LIST[int(gate)-1][0])
			for frm in formset:
				cli = frm.save(commit=False)
				cli.checklist = milestone
				# ^ could silently mess up if there are somehow two milestones on a project with the same name
				cli.save()
			milestone.completion_date = date.today()
			milestone.save()
			return HttpResponseRedirect('/projects/'+pid)
	else:
		# where will the defaults be located?
		checklist = GATE_LIST[int(gate)-1][1]
		init = {
			'form-TOTAL_FORMS':str(len(checklist)), # may need to be dynamic
			'form-INITIAL_FORMS':'0',
			'form-MIN_NUM_FORMS':'',
			'form-MAX_NUM_FORMS':'',
		}
		for i in range(len(checklist)):
			init['form-'+str(i)+'-name'] = checklist[i][0]
			init['form-'+str(i)+'-responsible'] = checklist[i][1]
			init['form-'+str(i)+'-completed'] = False
			init['form-'+str(i)+'-remarks'] = ''
			# don't know if the pre-existing remarks are supposed to be added or not
		formset = forms.ChecklistFormset(init)
	context = {'formset': formset, 'gate':{'number':gate, 'name':GATE_LIST[int(gate)-1][0]}, 'pid':pid, 'responsible':models.ChecklistItem.RESPONSIBLE}
	return render(request, 'projects/checklist.html', context)

@login_required
def download_checklist(request, pid, gate):
	proj = get_object_or_404(models.Project, pk=pid)
	ms = models.Milestone.objects.filter(project=pid).get(description=GATE_LIST[int(gate)-1][0])
	if ms.is_complete():
		filename = proj.name + ' - ' + GATE_LIST[int(gate)-1][0] + ' Gate Checklist.xlsx'
		response = HttpResponse(generate_gate_checklist(ms), content_type='application/vnd.ms-excel')
		response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
		return response
	elif not ms.is_complete():
		pass
		#raise error

KICKOFF = (
	('Gate 1 Check List Approved and Released', 'ENG'),
	('Kick-off Form Complete', 'ENG'),
	('Kick-off Meeting Between LZ and Factory Complete', 'ENG'),
	('Factory Kick-off Meeting Complete', 'ENG'),
	('Project Schedule has been Created and Agreed by Customer', 'ENG'),
	('DFM / DFA Feedback Complete', 'ENG'),
	('Customer Has Approved DFM & DFA Feedbacks', 'ENG'),
	('Document Numbers Have Been Created and Added to the BOM', 'ENG'),
	('BOM Has Been Created & Loaded in ERP System ', 'ENG'),
	('AVL loaded and Verified ', 'PUR'),
	('BOM Has Been Reviewed and Verified ', 'ENG'),
	('BOM Has Been Released in ERP System via ECO', 'ENG'),
	('Proto Build Requirement?', 'ENG'),
	('All Customer Documents Released to DCC', 'ENG'),
)
ENG_SAMPLES = (
	('Gate 2 Check List Approved and Released', 'ENG'),
	('DFM / DFA Completed & Approved', 'ENG'),
	('Tool Design Completed & Approved', 'ENG'),
	('Mold Flow Analysis Completed & Approved', 'ENG'),
	('ICT Test Defined & Implemented', 'ENG'),
	('Functional Test Defined & Implemented', 'ENG'),
	('E-Samples Shipped to Customer', 'ENG'),
	('1st Article Reports Completed and Sent to Customer', 'ENG'),
	('E-Samples Approval Form Sent to Customer', 'ENG'),
	('Customer Approval to Purchase Raw Materials for Production', 'ENG'),
	('Work Instructions Verified and Released', 'ENG'),
	('BOM Verified and Released to DCC', 'ENG'),
	('Component Specs (Mech. & Elec.) Approved and Released to DCC', 'ENG'),
	('Packaging Design Completed & Released', 'ENG'),
	('E-Samples Shipped in Final Packaging', 'ENG'),
	('Serial Number Labels Defined & Implemented', 'ENG'),
	('Pallet Size Defined & Documented', 'ENG'),
	('Labeling, Bar Code Specs Defined & Documented', 'ENG'),
	('New Printers, Barcode Scanners etc. Required ?', 'ENG'),
	('DMR Approved and Released  (Required for Medical Devices)', 'ENG'),
	('Risk Analysis Completed & Released', 'ENG'),
	('Process FMEA Verified & Released', 'ENG'),
	('Control Plan Verified & Released', 'ENG'),
	('Production Sampling Plan Defined', 'ENG'),
	('ESD Requirements Defined', 'ENG'),
	('Customer Service Notified to Send Tooling & E-Sample Invoices', 'ENG'),
	('Customer Approval of E-Samples Have Been Received', 'ENG'),
	('IQC Inspection Instructions Verified & Released', 'QLT'),
	('First Article Inspection Verified & Released', 'QLT'),
	('Quality Inspection Instructions Verified & Released', 'QLT'),
	('Quality Measurement Fixtures Created & Verified', 'QLT'),
	('Quality Standards Defined (Customer or IPC-A-610D)', 'QLT'),
	('Certificate of Conformance(s) Required?', 'QLT'),
	('Material Std Cost Loaded in ERP', 'PUR'),
	('Lead-Time Loaded in ERP and Verified', 'PUR'),
	('Local New Suppliers Audited & Approved?', 'PUR'),
	('All PO\'s Placed and Confirmed? Pilot Runs & Production Run', 'PUR'),
	('ICT Platform defined If Required', 'ME'),
	('ICT Fixture in house If Required', 'ME'),
	('ICT Test program Validated', 'ME'),
	('ICT test procedure released & verified ICT', 'ME'),
	('Troubleshoot Training Completed', 'ME'),
	('List of Components Which Can Not be Tested Provided', 'ME'),
	('Assembly and Test Fixtures Have been Created', 'ME'),
	('Test Equipment is Defined & Validated', 'ME'),
	('Test program is Defined & Validated', 'ME'),
	('Functional Testing Procedure Released & Verified', 'ME'),
)
QUALIFICATION = (
	('Gate 3 Check List Approved and Released', 'ENG'),
	('List of Customer Consigned Equipment', 'ME'),
	('Calibration Record for all Required Production Equipment', 'ME'),
	('SMT Program Defined & Verified', 'PRD'),
	('Stencil in house & Verified', 'PRD'),
	('Solder Paste Type Defined & Verified', 'PRD'),
	('Machine Set-up and Process Defined & Verified', 'PRD'),
	('Feeder & Nozzles Requirements Meet the Need', 'PRD'),
	('Special Nozzle & Feeder Requirements Defined & Verified, if any', 'PRD'),
	('Profile Completed & Verified', 'PRD'),
	('AOI Program Completed & Verified', 'PRD'),
	('Wave Carriers/Pallets Defined', 'PRD'),
	('Flux Type Defined', 'PRD'),
	('Water Cleaning or any Special Requirements Defined & Verified', 'PRD'),
	('No-Clean Flux Has Been Defined & Verified', 'PRD'),
	('Any Special Equipment & Training', 'PRD'),
	('Inspection Jig/Fixture/Template', 'PRD'),
	('Operation Tools & Fixture', 'PRD'),
	('Component Handling Defined & Verified', 'PRD'),
	('Work instructions Verified', 'PRD'),
	('Quality Bulletin for changes', 'QLT'),
	('Consumables (labels,ribbon,box,etc.)', 'PMC'),
	('Line Setup (conveyors & workbenches)', 'PRD'),
	('Setup Rework Stations (Touch up)', 'PRD'),
	('Line Set Up (equipment,etc.)', 'PRD'),
	('Tool setup (screwdrivers,fixtures,etc.)', 'PRD'),
	('Line Balance (Time study)', 'PRD'),
	('Material Flow on Line', 'PRD'),
	('Flow Chart Review', 'PRD'),
	('Work Instruction For Machine Defined', 'PRD'),
	('Indirect Material List Defined', 'PRD'),
	('Production Line Layout Defined', 'PRD'),
	('SMT Line Balanced and Headcount Defined', 'PRD'),
	('Packaging Area Balanced', 'PRD'),
	('Rework Area Balanced', 'PRD'),
	('Production Cycle Time Defined', 'PRD'),
	('Production Line Capacity Defined', 'PRD'),
	('Operators Trained and Certified', 'PRD'),
	('Production Line Audit Before QA audit', 'PRD'),
	('Production Line Scheduled', 'PMC'),
	('Production Line Scheduled', 'PMC'),
	('The Date for Receive Material at Plant', 'PMC'),
	('Define Build Quantity', 'PMC'),
	('Inventory Status of Consigned Material', 'PMC'),
	('Provide Customer Copy of Consigned Inventory', 'PMC'),
	('Functional Test Fixture GR&R Completed', 'QLT'),
	('PPAP Documents Approved and Released', 'ENG'),
	('Process Validation Document Approved and Released', 'ENG'),
	('IQ Reports Approved and Released (Required for Medical Devices)', 'ENG'),
	('OQ Reports Approved and Released (Required for Medical Devices)', 'ENG'),
	('PQ Reports Approved and Released (Required for Medical Devices)', 'ENG'),
	('DHR Approved and Released (Required for Medical Devices)', 'PRD'),
	('Process Audit Has Been Performed', 'QLT'),
)
PILOT = (
	('Gate 4 Check List Approved and Released', 'ENG'),
	('Component Incoming Inspections have been Reviewed & Released', 'ENG'),
	('ERP BOM has been Checked, Verified & Released', 'ENG'),
	('Work Instructions have been Checked, Verified & Released', 'ENG'),
	('DMR Document is Verified, Approved and Released', 'ENG'),
	('Customer Approval Form Has been Sent and Received', 'ENG'),
	('Raw Materials is Ready for 1st Production', 'PMC'),
	('Production Line Layout is Confirmed and Verified', 'PRD'),
	('Production Line Setup is Confirmed and Verified', 'PRD'),
	('Production Line Balance is Confirmed and Verified', 'PRD'),
	('Operators Trained and Certified', 'PRD'),
	('Production Fixtures have been verified', 'PRD'),
	('Pilot Run Units Have been Shipped to Customer', 'PRD'),
	('Pilot Run Yield Data has been collected, Analyzed and Approved', 'QLT'),
	('Pilot Run Summary Report has been issued and Released to DCC', 'QLT'),
	('Quality Work Instructions have been Checked, Verified & Released', 'QLT'),
	('DHR Approved and Released (Required for MedicalDevices)', 'QLT'),
	('COC Approved and Released (Required for MedicalDevices)', 'QLT'),
)
PRODUCTION = (
	('Gate 5 Check List Approved and Released', 'ENG'),
	('Work Instructions have Corrected via ECO and Released', 'ENG'),
	('ERP BOM has been Checked, Verified & Released', 'ENG'),
	('DMR Document is Verified, Approved and Released', 'ENG'),
	('Production Line Balance is Confirmed and Verified', 'PRD'),
	('Production Fixtures have been verified', 'PRD'),
	('1st Production Units Have been Shipped to Customer', 'PRD'),
	('1st Production run Data collected, Analyzed and Approved', 'QLT'),
	('Quality Work Instructions have been Checked, Verified & Released', 'QLT'),
	('DHR Approved and Released (Required for MedicalDevices)', 'QLT'),
	('COC Approved and Released (Required for MedicalDevices)', 'QLT'),
)
GATE_LIST = (
	('Kick-off', KICKOFF),
	('Engineering Samples', ENG_SAMPLES),
	('Qualification', QUALIFICATION),
	('Pilot Run', PILOT),
	('First Production', PRODUCTION),
)