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
		
	project = models.ForeignKey(Project, on_delete=models.PROTECT, verbose_name=_('project'))
	description = models.CharField(max_length=50, verbose_name=_('milestone'))
	deadline = models.DateField(verbose_name=_('deadline'))
	completion_date = models.DateField(blank=True, null=True, verbose_name=_('completion date'))
		
	def __str__(self):
		return self.project.name + ' - ' + self.description

	def is_complete(self):
		for item in self.checklist.all():
			if not item.completed:
				return item.completed
		else:
			return self.checklist.all().count() != 0


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


KICKOFF = (
	('Gate 1 Check List Approved and Released', 'Engineering'),
	('Kick-off Form Complete', 'Engineering'),
	('Kick-off Meeting Between LZ and Factory Complete', 'Engineering'),
	('Factory Kick-off Meeting Complete', 'Engineering'),
	('Project Schedule has been Created and Agreed by Customer', 'Engineering'),
	('DFM / DFA Feedback Complete', 'Engineering'),
	('Customer Has Approved DFM & DFA Feedbacks', ''),
	('Document Numbers Have Been Created and Added to the BOM', 'Engineering'),
	('BOM Has Been Created & Loaded in ERP System ', 'Engineering'),
	('AVL loaded and Verified ', 'Purchasing'),
	('BOM Has Been Reviewed and Verified ', 'Engineering'),
	('BOM Has Been Released in ERP System via ECO', 'Engineering'),
	('Proto Build Requirement?', 'Engineering'),
	('All Customer Documents Released to DCC', 'Engineering'),
)
ENG_SAMPLES = (
	('Gate 2 Check List Approved and Released', 'Engineering'),
	('DFM / DFA Completed & Approved', 'Engineering'),
	('Tool Design Completed & Approved', 'Engineering'),
	('Mold Flow Analysis Completed & Approved', 'Engineering'),
	('ICT Test Defined & Implemented', 'Engineering'),
	('Functional Test Defined & Implemented', 'Engineering'),
	('E-Samples Shipped to Customer', 'Engineering'),
	('1st Article Reports Completed and Sent to Customer', 'Engineering'),
	('E-Samples Approval Form Sent to Customer', 'Engineering'),
	('Customer Approval to Purchase Raw Materials for Production', 'Engineering'),
	('Work Instructions Verified and Released', 'Engineering'),
	('BOM Verified and Released to DCC', 'Engineering'),
	('Component Specs (Mech. & Elec.) Approved and Released to DCC', 'Engineering'),
	('Packaging Design Completed & Released', 'Engineering'),
	('E-Samples Shipped in Final Packaging', 'Engineering'),
	('Serial Number Labels Defined & Implemented', 'Engineering'),
	('Pallet Size Defined & Documented', 'Engineering'),
	('Labeling, Bar Code Specs Defined & Documented', 'Engineering'),
	('New Printers, Barcode Scanners etc. Required ?', 'Engineering'),
	('DMR Approved and Released  (Required for Medical Devices)', 'Engineering'),
	('Risk Analysis Completed & Released', 'Engineering'),
	('Process FMEA Verified & Released', 'Engineering'),
	('Control Plan Verified & Released', 'Engineering'),
	('Production Sampling Plan Defined', 'Engineering'),
	('ESD Requirements Defined', 'Engineering'),
	('Customer Service Notified to Send Tooling & E-Sample Invoices', 'Engineering'),
	('Customer Approval of E-Samples Have Been Received', 'Engineering'),
	('IQC Inspection Instructions Verified & Released', 'Quality'),
	('First Article Inspection Verified & Released', 'Quality'),
	('Quality Inspection Instructions Verified & Released', 'Quality'),
	('Quality Measurement Fixtures Created & Verified', 'Quality'),
	('Quality Standards Defined (Customer or IPC-A-610D)', 'Quality'),
	('Certificate of Conformance(s) Required?', 'Quality'),
	('Material Std Cost Loaded in ERP', 'Purchasing'),
	('Lead-Time Loaded in ERP and Verified', 'Purchasing'),
	('Local New Suppliers Audited & Approved?', 'Purchasing'),
	('All PO\'s Placed and Confirmed? Pilot Runs & Production Run', 'Purchasing'),
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
	('Gate 3 Check List Approved and Released', 'Engineering'),
	('List of Customer Consigned Equipment', 'ME'),
	('Calibration Record for all Required Production Equipment', 'ME'),
	('SMT Program Defined & Verified', 'Production'),
	('Stencil in house & Verified', 'Production'),
	('Solder Paste Type Defined & Verified', 'Production'),
	('Machine Set-up and Process Defined & Verified', 'Production'),
	('Feeder & Nozzles Requirements Meet the Need', 'Production'),
	('Special Nozzle & Feeder Requirements Defined & Verified, if any', 'Production'),
	('Profile Completed & Verified', 'Production'),
	('AOI Program Completed & Verified', 'Production'),
	('Wave Carriers/Pallets Defined', 'Production'),
	('Flux Type Defined', 'Production'),
	('Water Cleaning or any Special Requirements Defined & Verified', 'Production'),
	('No-Clean Flux Has Been Defined & Verified', 'Production'),
	('Any Special Equipment & Training', 'Production'),
	('Inspection Jig/Fixture/Template', 'Production'),
	('Operation Tools & Fixture', 'Production'),
	('Component Handling Defined & Verified', 'Production'),
	('Work instructions Verified', 'Production'),
	('Quality Bulletin for changes', 'Quality'),
	('Consumables (labels,ribbon,box,etc.)', 'PMC'),
	('Line Setup (conveyors & workbenches)', 'Production'),
	('Setup Rework Stations (Touch up)', 'Production'),
	('Line Set Up (equipment,etc.)', 'Production'),
	('Tool setup (screwdrivers,fixtures,etc.)', 'Production'),
	('Line Balance (Time study)', 'Production'),
	('Material Flow on Line', 'Production'),
	('Flow Chart Review', 'Production'),
	('Work Instruction For Machine Defined', 'Production'),
	('Indirect Material List Defined', 'Production'),
	('Production Line Layout Defined', 'Production'),
	('SMT Line Balanced and Headcount Defined', 'Production'),
	('Packaging Area Balanced', 'Production'),
	('Rework Area Balanced', 'Production'),
	('Production Cycle Time Defined', 'Production'),
	('Production Line Capacity Defined', 'Production'),
	('Operators Trained and Certified', 'Production'),
	('Production Line Audit Before QA audit', 'Production'),
	('Production Line Scheduled', 'PMC'),
	('Production Line Scheduled', 'PMC'),
	('The Date for Receive Material at Plant', 'PMC'),
	('Define Build Quantity', 'PMC'),
	('Inventory Status of Consigned Material', 'PMC'),
	('Provide Customer Copy of Consigned Inventory', 'PMC'),
	('Functional Test Fixture GR&R Completed', 'Quality'),
	('PPAP Documents Approved and Released', 'Engineering'),
	('Process Validation Document Approved and Released', 'Engineering'),
	('IQ Reports Approved and Released (Required for Medical Devices)', 'Engineering'),
	('OQ Reports Approved and Released (Required for Medical Devices)', 'Engineering'),
	('PQ Reports Approved and Released (Required for Medical Devices)', 'Engineering'),
	('DHR Approved and Released (Required for Medical Devices)', 'Production'),
	('Process Audit Has Been Performed', 'Quality'),
)
PILOT = (
	('', 'Engineering'),
	('', 'Engineering'),
	('', 'Engineering'),
	('', 'Engineering'),
	('', 'Engineering'),
	('', 'Engineering'),
	('', 'PMC'),
	('', 'Production'),
	('', 'Production'),
	('', 'Production'),
	('', 'Production'),
	('', 'Production'),
	('', 'Production'),
	('', 'Quality'),
	('', 'Quality'),
	('', 'Quality'),
	('', 'Quality'),
	('', 'Quality'),
)
PRODUCTION = (
	('', 'Engineering'),
	('', 'Engineering'),
	('', 'Engineering'),
	('', 'Engineering'),
	('', 'Production'),
	('', 'Production'),
	('', 'Production'),
	('', 'Quality'),
	('', 'Quality'),
	('', 'Quality'),
	('', 'Quality'),
)
GATE_LIST = (
	('Kick-off', KICKOFF),
	('Engineering Samples', ENG_SAMPLES),
	('Kick-off', QUALIFICATION),
	('Pilot Run', PILOT),
	('First Production', PRODUCTION),
)

class ChecklistItem(models.Model):
	"""represents a single item in a checklist"""
	class Meta:
		verbose_name = _('checklist item')
	
	RESPONSIBLE = (
		('ENG', 'Engineering'), 
		('QLT', 'Quality'),
		('PUR', 'Purchasing'),
		('ME', 'ME'),
		('PRD', 'Production'),
		('PMC', 'PMC'),
	)

	checklist = models.ForeignKey(Milestone, on_delete=models.PROTECT, verbose_name=_('checklist'), related_name='checklist')
	name = models.CharField(max_length=35, verbose_name=_('item'))
	responsible =  models.CharField(max_length=3, choices=RESPONSIBLE, verbose_name=_('responsible')) # multiselect field
	completed = models.NullBooleanField(verbose_name=_('is complete'))
	remarks = models.CharField(max_length=120, verbose_name=_('comments'))
		