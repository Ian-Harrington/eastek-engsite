from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from employees.models import Employee

class Defaults():
	"""class to store simple NPI/project defaults"""
	KICKOFF = (
		(_('Gate 1 Check List Approved and Released'), 'ENG'),
		(_('Kick-off Form Complete'), 'ENG'),
		(_('Kick-off Meeting Between LZ and Factory Complete'), 'ENG'),
		(_('Factory Kick-off Meeting Complete'), 'ENG'),
		(_('Project Schedule has been Created and Agreed by Customer'), 'ENG'),
		(_('DFM / DFA Feedback Complete'), 'ENG'),
		(_('Customer Has Approved DFM & DFA Feedbacks'), 'ENG'),
		(_('Document Numbers Have Been Created and Added to the BOM'), 'ENG'),
		(_('BOM Has Been Created & Loaded in ERP System'), 'ENG'),
		(_('AVL loaded and Verified'), 'PUR'),
		(_('BOM Has Been Reviewed and Verified'), 'ENG'),
		(_('BOM Has Been Released in ERP System via ECO'), 'ENG'),
		(_('Proto Build Requirement?'), 'ENG'),
		(_('All Customer Documents Released to DCC')_, 'ENG'),
	)
	ENG_SAMPLES = (
		(_('Gate 2 Check List Approved and Released'), 'ENG'),
		(_('DFM / DFA Completed & Approved'), 'ENG'),
		(_('Tool Design Completed & Approved'), 'ENG'),
		(_('Mold Flow Analysis Completed & Approved'), 'ENG'),
		(_('ICT Test Defined & Implemented'), 'ENG'),
		(_('Functional Test Defined & Implemented'), 'ENG'),
		(_('E-Samples Shipped to Customer'), 'ENG'),
		(_('1st Article Reports Completed and Sent to Customer'), 'ENG'),
		(_('E-Samples Approval Form Sent to Customer'), 'ENG'),
		(_('Customer Approval to Purchase Raw Materials for Production'), 'ENG'),
		(_('Work Instructions Verified and Released'), 'ENG'),
		(_('BOM Verified and Released to DCC'), 'ENG'),
		(_('Component Specs (Mech. & Elec.) Approved and Released to DCC'), 'ENG'),
		(_('Packaging Design Completed & Released'), 'ENG'),
		(_('E-Samples Shipped in Final Packaging'), 'ENG'),
		(_('Serial Number Labels Defined & Implemented'), 'ENG'),
		(_('Pallet Size Defined & Documented'), 'ENG'),
		(_('Labeling, Bar Code Specs Defined & Documented'), 'ENG'),
		(_('New Printers, Barcode Scanners etc. Required ?'), 'ENG'),
		(_('DMR Approved and Released  (Required for Medical Devices)'), 'ENG'),
		(_('Risk Analysis Completed & Released'), 'ENG'),
		(_('Process FMEA Verified & Released'), 'ENG'),
		(_('Control Plan Verified & Released'), 'ENG'),
		(_('Production Sampling Plan Defined'), 'ENG'),
		(_('ESD Requirements Defined'), 'ENG'),
		(_('Customer Service Notified to Send Tooling & E-Sample Invoices'), 'ENG'),
		(_('Customer Approval of E-Samples Have Been Received'), 'ENG'),
		(_('IQC Inspection Instructions Verified & Released'), 'QLT'),
		(_('First Article Inspection Verified & Released'), 'QLT'),
		(_('Quality Inspection Instructions Verified & Released'), 'QLT'),
		(_('Quality Measurement Fixtures Created & Verified'), 'QLT'),
		(_('Quality Standards Defined (Customer or IPC-A-610D)'), 'QLT'),
		(_('Certificate of Conformance(s) Required?'), 'QLT'),
		(_('Material Std Cost Loaded in ERP'), 'PUR'),
		(_('Lead-Time Loaded in ERP and Verified'), 'PUR'),
		(_('Local New Suppliers Audited & Approved?'), 'PUR'),
		(_('All PO\'s Placed and Confirmed? Pilot Runs & Production Run'), 'PUR'),
		(_('ICT Platform defined If Required'), 'ME'),
		(_('ICT Fixture in house If Required'), 'ME'),
		(_('ICT Test program Validated'), 'ME'),
		(_('ICT test procedure released & verified ICT'), 'ME'),
		(_('Troubleshoot Training Completed'), 'ME'),
		(_('List of Components Which Can Not be Tested Provided'), 'ME'),
		(_('Assembly and Test Fixtures Have been Created'), 'ME'),
		(_('Test Equipment is Defined & Validated'), 'ME'),
		(_('Test program is Defined & Validated'), 'ME'),
		(_('Functional Testing Procedure Released & Verified'), 'ME'),
	)
	QUALIFICATION = (
		(_('Gate 3 Check List Approved and Released'), 'ENG'),
		(_('List of Customer Consigned Equipment'), 'ME'),
		(_('Calibration Record for all Required Production Equipment'), 'ME'),
		(_('SMT Program Defined & Verified'), 'PRD'),
		(_('Stencil in house & Verified'), 'PRD'),
		(_('Solder Paste Type Defined & Verified'), 'PRD'),
		(_('Machine Set-up and Process Defined & Verified'), 'PRD'),
		(_('Feeder & Nozzles Requirements Meet the Need'), 'PRD'),
		(_('Special Nozzle & Feeder Requirements Defined & Verified, if any'), 'PRD'),
		(_('Profile Completed & Verified'), 'PRD'),
		(_('AOI Program Completed & Verified'), 'PRD'),
		(_('Wave Carriers/Pallets Defined'), 'PRD'),
		(_('Flux Type Defined'), 'PRD'),
		(_('Water Cleaning or any Special Requirements Defined & Verified'), 'PRD'),
		(_('No-Clean Flux Has Been Defined & Verified'), 'PRD'),
		(_('Any Special Equipment & Training'), 'PRD'),
		(_('Inspection Jig/Fixture/Template'), 'PRD'),
		(_('Operation Tools & Fixture'), 'PRD'),
		(_('Component Handling Defined & Verified'), 'PRD'),
		(_('Work instructions Verified'), 'PRD'),
		(_('Quality Bulletin for changes'), 'QLT'),
		(_('Consumables (labels,ribbon,box,etc.)'), 'PMC'),
		(_('Line Setup (conveyors & workbenches)'), 'PRD'),
		(_('Setup Rework Stations (Touch up)'), 'PRD'),
		(_('Line Set Up (equipment,etc.)'), 'PRD'),
		(_('Tool setup (screwdrivers,fixtures,etc.)'), 'PRD'),
		(_('Line Balance (Time study)'), 'PRD'),
		(_('Material Flow on Line'), 'PRD'),
		(_('Flow Chart Review'), 'PRD'),
		(_('Work Instruction For Machine Defined'), 'PRD'),
		(_('Indirect Material List Defined'), 'PRD'),
		(_('Production Line Layout Defined'), 'PRD'),
		(_('SMT Line Balanced and Headcount Defined'), 'PRD'),
		(_('Packaging Area Balanced'), 'PRD'),
		(_('Rework Area Balanced'), 'PRD'),
		(_('Production Cycle Time Defined'), 'PRD'),
		(_('Production Line Capacity Defined'), 'PRD'),
		(_('Operators Trained and Certified'), 'PRD'),
		(_('Production Line Audit Before QA audit'), 'PRD'),
		(_('Production Line Scheduled'), 'PMC'),
		(_('The Date for Receive Material at Plant'), 'PMC'),
		(_('Define Build Quantity'), 'PMC'),
		(_('Inventory Status of Consigned Material'), 'PMC'),
		(_('Provide Customer Copy of Consigned Inventory'), 'PMC'),
		(_('Functional Test Fixture GR&R Completed'), 'QLT'),
		(_('PPAP Documents Approved and Released'), 'ENG'),
		(_('Process Validation Document Approved and Released'), 'ENG'),
		(_('IQ Reports Approved and Released (Required for Medical Devices)'), 'ENG'),
		(_('OQ Reports Approved and Released (Required for Medical Devices)'), 'ENG'),
		(_('PQ Reports Approved and Released (Required for Medical Devices)'), 'ENG'),
		(_('DHR Approved and Released (Required for Medical Devices)'), 'PRD'),
		(_('Process Audit Has Been Performed'), 'QLT'),
	)
	PILOT = (
		(_('Gate 4 Check List Approved and Released'), 'ENG'),
		(_('Component Incoming Inspections have been Reviewed & Released'), 'ENG'),
		(_('ERP BOM has been Checked, Verified & Released'), 'ENG'),
		(_('Work Instructions have been Checked, Verified & Released'), 'ENG'),
		(_('DMR Document is Verified, Approved and Released'), 'ENG'),
		(_('Customer Approval Form Has been Sent and Received'), 'ENG'),
		(_('Raw Materials is Ready for 1st Production'), 'PMC'),
		(_('Production Line Layout is Confirmed and Verified'), 'PRD'),
		(_('Production Line Setup is Confirmed and Verified'), 'PRD'),
		(_('Production Line Balance is Confirmed and Verified'), 'PRD'),
		(_('Operators Trained and Certified'), 'PRD'),
		(_('Production Fixtures have been verified'), 'PRD'),
		(_('Pilot Run Units Have been Shipped to Customer'), 'PRD'),
		(_('Pilot Run Yield Data has been collected, Analyzed and Approved'), 'QLT'),
		(_('Pilot Run Summary Report has been issued and Released to DCC'), 'QLT'),
		(_('Quality Work Instructions have been Checked, Verified & Released'), 'QLT'),
		(_('DHR Approved and Released (Required for MedicalDevices)'), 'QLT'),
		(_('COC Approved and Released (Required for MedicalDevices)'), 'QLT'),
	)
	PRODUCTION = (
		(_('Gate 5 Check List Approved and Released'), 'ENG'),
		(_('Work Instructions have Corrected via ECO and Released'), 'ENG'),
		(_('ERP BOM has been Checked, Verified & Released'), 'ENG'),
		(_('DMR Document is Verified, Approved and Released'), 'ENG'),
		(_('Production Line Balance is Confirmed and Verified'), 'PRD'),
		(_('Production Fixtures have been verified'), 'PRD'),
		(_('1st Production Units Have been Shipped to Customer'), 'PRD'),
		(_('1st Production run Data collected, Analyzed and Approved'), 'QLT'),
		(_('Quality Work Instructions have been Checked, Verified & Released'), 'QLT'),
		(_('DHR Approved and Released (Required for MedicalDevices)'), 'QLT'),
		(_('COC Approved and Released (Required for MedicalDevices)'), 'QLT'),
	)
	GATE_LIST = (
		(_('Kick-off'), KICKOFF),
		(_('Engineering Samples'), ENG_SAMPLES),
		(_('Qualification'), QUALIFICATION),
		(_('Pilot Run'), PILOT),
		(_('First Production'), PRODUCTION),
	)
	WORK_REASON = (
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
	lead_eng = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name=_('lead engineer'))
	engineer = models.ManyToManyField(Employee, blank=True, verbose_name=_('engineer(s)'))
	#estimated_hours = models.SmallIntegerField(null=True, verbose_name=_('estimated hours'))
	eastek_pn = models.CharField(max_length=45, blank=True, verbose_name=_('eastek part number'))
	cust_pn = models.CharField(max_length=45, blank=True, verbose_name=_('customer part number'))

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
		
	project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=_('project'))
	description = models.CharField(max_length=50, verbose_name=_('milestone'))
	deadline = models.DateField(verbose_name=_('deadline'))
	completion_date = models.DateField(blank=True, null=True, verbose_name=_('completion date'))
	
	def __str__(self):
		return self.project.name + ' - ' + self.description

	def is_complete(self):
		for item in self.checklist.all():
			if item.completed != None and not item.completed:
				return item.completed
		else:
			return self.checklist.all().count() != 0


class Update(models.Model):
	"""stores project updates and meta"""
	class Meta:
		ordering = ['-mod_date']
		verbose_name = _('update')

	STAGES = Defaults.WORK_REASON
	project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=_('project')) # filled automatically
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


class ChecklistItem(models.Model):
	"""represents a single item in a checklist"""
	class Meta:
		verbose_name = _('checklist item')
	
	RESPONSIBLE = (
		('ENG', _('Engineering')), 
		('QLT', _('Quality')),
		('PUR', _('Purchasing')),
		('ME', _('ME')),
		('PRD', _('Production')),
		('PMC', _('PMC')),
	)

	COMP_CHOICE = (
		(True, 'Yes'),
		('False', 'No'),
		('None', 'N/A'),
	)

	checklist = models.ForeignKey(Milestone, on_delete=models.CASCADE, verbose_name=_('checklist'), related_name='checklist')
	name = models.CharField(max_length=70, verbose_name=_('item'))
	responsible =  models.CharField(max_length=3, choices=RESPONSIBLE, verbose_name=_('responsible')) # multiselect field
	completed = models.NullBooleanField(blank=True, null=True, choices=COMP_CHOICE, verbose_name=_('is complete'))
	remarks = models.CharField(max_length=120, blank=True, verbose_name=_('comments'))
	
	def __str__(self):
		return self.checklist.description + ' - ' + self.name
