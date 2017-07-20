from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from employees.models import Employee

class Defaults():
	"""class to store simple NPI/project defaults"""
	KICKOFF = (
		('g1-q1', 'ENG'),
		('g1-q2', 'ENG'),
		('g1-q3', 'ENG'),
		('g1-q4', 'ENG'),
		('g1-q5', 'ENG'),
		('g1-q6', 'ENG'),
		('g1-q7', 'ENG'),
		('g1-q8', 'ENG'),
		('g1-q9', 'ENG'),
		('g1-q10', 'PUR'),
		('g1-q11', 'ENG'),
		('g1-q12', 'ENG'),
		('g1-q13', 'ENG'),
		('g1-q14', 'ENG'),
	)
	G1_TRANS = (
		('g1-q1', _('Gate 1 Check List Approved and Released')),
		('g1-q2', _('Kick-off Form Complete')),
		('g1-q3', _('Kick-off Meeting Between LZ and Factory Complete')),
		('g1-q4', _('Factory Kick-off Meeting Complete')),
		('g1-q5', _('Project Schedule has been Created and Agreed by Customer')),
		('g1-q6', _('DFM / DFA Feedback Complete')),
		('g1-q7', _('Customer Has Approved DFM & DFA Feedbacks')),
		('g1-q8', _('Document Numbers Have Been Created and Added to the BOM')),
		('g1-q9', _('BOM Has Been Created & Loaded in ERP System')),
		('g1-q10', _('AVL loaded and Verified')),
		('g1-q11', _('BOM Has Been Reviewed and Verified')),
		('g1-q12', _('BOM Has Been Released in ERP System via ECO')),
		('g1-q13', _('Proto Build Requirement?')),
		('g1-q14', _('All Customer Documents Released to DCC')),
	)
	ENG_SAMPLES = (
		('g2-q1', 'ENG'),
		('g2-q2', 'ENG'),
		('g2-q3', 'ENG'),
		('g2-q4', 'ENG'),
		('g2-q5', 'ENG'),
		('g2-q6', 'ENG'),
		('g2-q7', 'ENG'),
		('g2-q8', 'ENG'),
		('g2-q9', 'ENG'),
		('g2-q10', 'ENG'),
		('g2-q11', 'ENG'),
		('g2-q12', 'ENG'),
		('g2-q13', 'ENG'),
		('g2-q14', 'ENG'),
		('g2-q15', 'ENG'),
		('g2-q16', 'ENG'),
		('g2-q17', 'ENG'),
		('g2-q18', 'ENG'),
		('g2-q19', 'ENG'),
		('g2-q20', 'ENG'),
		('g2-q21', 'ENG'),
		('g2-q22', 'ENG'),
		('g2-q23', 'ENG'),
		('g2-q24', 'ENG'),
		('g2-q25', 'ENG'),
		('g2-q26', 'ENG'),
		('g2-q27', 'ENG'),
		('g2-q28', 'QLT'),
		('g2-q29', 'QLT'),
		('g2-q30', 'QLT'),
		('g2-q31', 'QLT'),
		('g2-q32', 'QLT'),
		('g2-q33', 'QLT'),
		('g2-q34', 'PUR'),
		('g2-q35', 'PUR'),
		('g2-q36', 'PUR'),
		('g2-q37', 'PUR'),
		('g2-q38', 'ME'),
		('g2-q39', 'ME'),
		('g2-q40', 'ME'),
		('g2-q41', 'ME'),
		('g2-q42', 'ME'),
		('g2-q43', 'ME'),
		('g2-q44', 'ME'),
		('g2-q45', 'ME'),
		('g2-q46', 'ME'),
		('g2-q47', 'ME'),
	)
	G2_TRANS = (
		('g2-q1', _('Gate 2 Check List Approved and Released')),
		('g2-q2', _('DFM / DFA Completed & Approved')),
		('g2-q3', _('Tool Design Completed & Approved')),
		('g2-q4', _('Mold Flow Analysis Completed & Approved')),
		('g2-q5', _('ICT Test Defined & Implemented')),
		('g2-q6', _('Functional Test Defined & Implemented')),
		('g2-q7', _('E-Samples Shipped to Customer')),
		('g2-q8', _('1st Article Reports Completed and Sent to Customer')),
		('g2-q9', _('E-Samples Approval Form Sent to Customer')),
		('g2-q10', _('Customer Approval to Purchase Raw Materials for Production')),
		('g2-q11', _('Work Instructions Verified and Released')),
		('g2-q12', _('BOM Verified and Released to DCC')),
		('g2-q13', _('Component Specs (Mech. & Elec.) Approved and Released to DCC')),
		('g2-q14', _('Packaging Design Completed & Released')),
		('g2-q15', _('E-Samples Shipped in Final Packaging')),
		('g2-q16', _('Serial Number Labels Defined & Implemented')),
		('g2-q17', _('Pallet Size Defined & Documented')),
		('g2-q18', _('Labeling, Bar Code Specs Defined & Documented')),
		('g2-q19', _('New Printers, Barcode Scanners etc. Required ?')),
		('g2-q20', _('DMR Approved and Released  (Required for Medical Devices)')),
		('g2-q21', _('Risk Analysis Completed & Released')),
		('g2-q22', _('Process FMEA Verified & Released')),
		('g2-q23', _('Control Plan Verified & Released')),
		('g2-q24', _('Production Sampling Plan Defined')),
		('g2-q25', _('ESD Requirements Defined')),
		('g2-q26', _('Customer Service Notified to Send Tooling & E-Sample Invoices')),
		('g2-q27', _('Customer Approval of E-Samples Have Been Received')),
		('g2-q28', _('IQC Inspection Instructions Verified & Released')),
		('g2-q29', _('First Article Inspection Verified & Released')),
		('g2-q30', _('Quality Inspection Instructions Verified & Released')),
		('g2-q31', _('Quality Measurement Fixtures Created & Verified')),
		('g2-q32', _('Quality Standards Defined (Customer or IPC-A-610D)')),
		('g2-q33', _('Certificate of Conformance(s) Required?')),
		('g2-q34', _('Material Std Cost Loaded in ERP')),
		('g2-q35', _('Lead-Time Loaded in ERP and Verified')),
		('g2-q36', _('Local New Suppliers Audited & Approved?')),
		('g2-q37', _('All PO\'s Placed and Confirmed? Pilot Runs & Production Run')),
		('g2-q38', _('ICT Platform defined If Required')),
		('g2-q39', _('ICT Fixture in house If Required')),
		('g2-q40', _('ICT Test program Validated')),
		('g2-q41', _('ICT test procedure released & verified ICT')),
		('g2-q42', _('Troubleshoot Training Completed')),
		('g2-q43', _('List of Components Which Can Not be Tested Provided')),
		('g2-q44', _('Assembly and Test Fixtures Have been Created')),
		('g2-q45', _('Test Equipment is Defined & Validated')),
		('g2-q46', _('Test program is Defined & Validated')),
		('g2-q47', _('Functional Testing Procedure Released & Verified')),
	)
	QUALIFICATION = (
		('g3-q1', 'ENG'),
		('g3-q2', 'ME'),
		('g3-q3', 'ME'),
		('g3-q4', 'PRD'),
		('g3-q5', 'PRD'),
		('g3-q6', 'PRD'),
		('g3-q7', 'PRD'),
		('g3-q8', 'PRD'),
		('g3-q9', 'PRD'),
		('g3-q10', 'PRD'),
		('g3-q11', 'PRD'),
		('g3-q12', 'PRD'),
		('g3-q13', 'PRD'),
		('g3-q14', 'PRD'),
		('g3-q15', 'PRD'),
		('g3-q16', 'PRD'),
		('g3-q17', 'PRD'),
		('g3-q18', 'PRD'),
		('g3-q19', 'PRD'),
		('g3-q20', 'PRD'),
		('g3-q21', 'QLT'),
		('g3-q22', 'PMC'),
		('g3-q23', 'PRD'),
		('g3-q24', 'PRD'),
		('g3-q25', 'PRD'),
		('g3-q26', 'PRD'),
		('g3-q27', 'PRD'),
		('g3-q28', 'PRD'),
		('g3-q29', 'PRD'),
		('g3-q30', 'PRD'),
		('g3-q31', 'PRD'),
		('g3-q32', 'PRD'),
		('g3-q33', 'PRD'),
		('g3-q34', 'PRD'),
		('g3-q35', 'PRD'),
		('g3-q36', 'PRD'),
		('g3-q37', 'PRD'),
		('g3-q38', 'PRD'),
		('g3-q39', 'PRD'),
		('g3-q40', 'PMC'),
		('g3-q41', 'PMC'),
		('g3-q42', 'PMC'),
		('g3-q43', 'PMC'),
		('g3-q44', 'PMC'),
		('g3-q45', 'QLT'),
		('g3-q46', 'ENG'),
		('g3-q47', 'ENG'),
		('g3-q48', 'ENG'),
		('g3-q49', 'ENG'),
		('g3-q50', 'ENG'),
		('g3-q51', 'PRD'),
		('g3-q52', 'QLT'),
	)
	G3_TRANS = (
		('g3-q1', _('Gate 3 Check List Approved and Released')),
		('g3-q2', _('List of Customer Consigned Equipment')),
		('g3-q3', _('Calibration Record for all Required Production Equipment')),
		('g3-q4', _('SMT Program Defined & Verified')),
		('g3-q5', _('Stencil in house & Verified')),
		('g3-q6', _('Solder Paste Type Defined & Verified')),
		('g3-q7', _('Machine Set-up and Process Defined & Verified')),
		('g3-q8', _('Feeder & Nozzles Requirements Meet the Need')),
		('g3-q9', _('Special Nozzle & Feeder Requirements Defined & Verified, if any')),
		('g3-q10', _('Profile Completed & Verified')),
		('g3-q11', _('AOI Program Completed & Verified')),
		('g3-q12', _('Wave Carriers/Pallets Defined')),
		('g3-q13', _('Flux Type Defined')),
		('g3-q14', _('Water Cleaning or any Special Requirements Defined & Verified')),
		('g3-q15', _('No-Clean Flux Has Been Defined & Verified')),
		('g3-q16', _('Any Special Equipment & Training')),
		('g3-q17', _('Inspection Jig/Fixture/Template')),
		('g3-q18', _('Operation Tools & Fixture')),
		('g3-q19', _('Component Handling Defined & Verified')),
		('g3-q20', _('Work instructions Verified')),
		('g3-q21', _('Quality Bulletin for changes')),
		('g3-q22', _('Consumables (labels,ribbon,box,etc.)')),
		('g3-q23', _('Line Setup (conveyors & workbenches)')),
		('g3-q24', _('Setup Rework Stations (Touch up)')),
		('g3-q25', _('Line Set Up (equipment,etc.)')),
		('g3-q26', _('Tool setup (screwdrivers,fixtures,etc.)')),
		('g3-q27', _('Line Balance (Time study)')),
		('g3-q28', _('Material Flow on Line')),
		('g3-q29', _('Flow Chart Review')),
		('g3-q30', _('Work Instruction For Machine Defined')),
		('g3-q31', _('Indirect Material List Defined')),
		('g3-q32', _('Production Line Layout Defined')),
		('g3-q33', _('SMT Line Balanced and Headcount Defined')),
		('g3-q34', _('Packaging Area Balanced')),
		('g3-q35', _('Rework Area Balanced')),
		('g3-q36', _('Production Cycle Time Defined')),
		('g3-q37', _('Production Line Capacity Defined')),
		('g3-q38', _('Operators Trained and Certified')),
		('g3-q39', _('Production Line Audit Before QA audit')),
		('g3-q40', _('Production Line Scheduled')),
		('g3-q41', _('The Date for Receive Material at Plant')),
		('g3-q42', _('Define Build Quantity')),
		('g3-q43', _('Inventory Status of Consigned Material')),
		('g3-q44', _('Provide Customer Copy of Consigned Inventory')),
		('g3-q45', _('Functional Test Fixture GR&R Completed')),
		('g3-q46', _('PPAP Documents Approved and Released')),
		('g3-q47', _('Process Validation Document Approved and Released')),
		('g3-q48', _('IQ Reports Approved and Released (Required for Medical Devices)')),
		('g3-q49', _('OQ Reports Approved and Released (Required for Medical Devices)')),
		('g3-q50', _('PQ Reports Approved and Released (Required for Medical Devices)')),
		('g3-q51', _('DHR Approved and Released (Required for Medical Devices)')),
		('g3-q52', _('Process Audit Has Been Performed')),
	)
	PILOT = (
		('g4-q1', 'ENG'),
		('g4-q2', 'ENG'),
		('g4-q3', 'ENG'),
		('g4-q4', 'ENG'),
		('g4-q5', 'ENG'),
		('g4-q6', 'ENG'),
		('g4-q7', 'PMC'),
		('g4-q8', 'PRD'),
		('g4-q9', 'PRD'),
		('g4-q10', 'PRD'),
		('g4-q11', 'PRD'),
		('g4-q12', 'PRD'),
		('g4-q13', 'PRD'),
		('g4-q14', 'QLT'),
		('g4-q15', 'QLT'),
		('g4-q16', 'QLT'),
		('g4-q17', 'QLT'),
		('g4-q18', 'QLT'),
	)
	G4_TRANS = (
		('g4-q1', _('Gate 4 Check List Approved and Released')),
		('g4-q2', _('Component Incoming Inspections have been Reviewed & Released')),
		('g4-q3', _('ERP BOM has been Checked, Verified & Released')),
		('g4-q4', _('Work Instructions have been Checked, Verified & Released')),
		('g4-q5', _('DMR Document is Verified, Approved and Released')),
		('g4-q6', _('Customer Approval Form Has been Sent and Received')),
		('g4-q7', _('Raw Materials is Ready for 1st Production')),
		('g4-q8', _('Production Line Layout is Confirmed and Verified')),
		('g4-q9', _('Production Line Setup is Confirmed and Verified')),
		('g4-q10', _('Production Line Balance is Confirmed and Verified')),
		('g4-q11', _('Operators Trained and Certified')),
		('g4-q12', _('Production Fixtures have been verified')),
		('g4-q13', _('Pilot Run Units Have been Shipped to Customer')),
		('g4-q14', _('Pilot Run Yield Data has been collected, Analyzed and Approved')),
		('g4-q15', _('Pilot Run Summary Report has been issued and Released to DCC')),
		('g4-q16', _('Quality Work Instructions have been Checked, Verified & Released')),
		('g4-q17', _('DHR Approved and Released (Required for MedicalDevices)')),
		('g4-q18', _('COC Approved and Released (Required for MedicalDevices)')),
	)
	PRODUCTION = (
		('g5-q1', 'ENG'),
		('g5-q2', 'ENG'),
		('g5-q3', 'ENG'),
		('g5-q4', 'ENG'),
		('g5-q5', 'PRD'),
		('g5-q6', 'PRD'),
		('g5-q7', 'PRD'),
		('g5-q8', 'QLT'),
		('g5-q9', 'QLT'),
		('g5-q10', 'QLT'),
		('g5-q11', 'QLT'),
	)
	G5_TRANS = (
		('g5-q1', _('Gate 5 Check List Approved and Released')),
		('g5-q2', _('Work Instructions have Corrected via ECO and Released')),
		('g5-q3', _('ERP BOM has been Checked, Verified & Released')),
		('g5-q4', _('DMR Document is Verified, Approved and Released')),
		('g5-q5', _('Production Line Balance is Confirmed and Verified')),
		('g5-q6', _('Production Fixtures have been verified')),
		('g5-q7', _('1st Production Units Have been Shipped to Customer')),
		('g5-q8', _('1st Production run Data collected, Analyzed and Approved')),
		('g5-q9', _('Quality Work Instructions have been Checked, Verified & Released')),
		('g5-q10', _('DHR Approved and Released (Required for MedicalDevices)')),
		('g5-q11', _('COC Approved and Released (Required for MedicalDevices)')),
	)
	GATE_LIST = (
		('Kick-off', KICKOFF, G1_TRANS),
		('Engineering Samples', ENG_SAMPLES, G2_TRANS),
		('Qualification', QUALIFICATION, G3_TRANS),
		('Pilot Run', PILOT, G4_TRANS),
		('First Production', PRODUCTION, G5_TRANS),
	)
	RESPONSIBLE = (
		('ENG', _('Engineering')), 
		('QLT', _('Quality')),
		('PUR', _('Purchasing')),
		('ME', _('ME')),
		('PRD', _('Production')),
		('PMC', _('PMC')),
	)
	WORK_REASON = (
		('RPCST', _('Responding to Customer')), 
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
		('M', _('Mechanical')),
		('E', _('Electronic')),
		('A', _('Assembly')),
		('ME', str(_('Mechanical'))+'/'+str(_('Electronic'))),
		('MA', str(_('Mechanical'))+'/'+str(_('Assembly'))),
		('EA', str(_('Electronic'))+'/'+str(_('Assembly'))),
		('MEA', str(_('Mechanical'))+'/'+str(_('Electronic'))+'/'+str(_('Assembly'))),
	)
	STATUS = (
		('INP', _('In-Progress')),
		('HLD', _('On Hold')),
		('CND', _('Cancelled')),
		('CMP', _('Completed'))
	)
	name = models.CharField(max_length=120, verbose_name=_('project name')) #name or PN (need to improve)
	customer = models.ForeignKey('Customer', on_delete=models.PROTECT, verbose_name=_('customer'))
	work_type = models.CharField(max_length=3, choices=WORK_TYPES, verbose_name=_('project type'))
	status = models.CharField(max_length=3, choices=STATUS, verbose_name=_('status'))
	#lead_eng = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name=_('lead engineer'), related_name='project_leader')
	engineer = models.ManyToManyField(Employee, blank=True, verbose_name=_('engineer(s)'), related_name='project_member')
	#estimated_hours = models.SmallIntegerField(null=True, verbose_name=_('estimated hours'))
	eastek_pn = models.CharField(max_length=85, blank=True, verbose_name=_('eastek part number'))
	cust_pn = models.CharField(max_length=85, blank=True, verbose_name=_('customer part number'))

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
	deadline = models.DateField(blank=True, null=True, verbose_name=_('deadline'))
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
	name = models.CharField(max_length=80, unique=True, verbose_name=_('customer'))

	class Meta:
		verbose_name = _('customer')
	
	def __str__(self):
		return self.name


class ChecklistItem(models.Model):
	"""represents a single item in a checklist"""
	class Meta:
		verbose_name = _('checklist item')

	COMP_CHOICE = (
		(True, 'Yes'),
		('False', 'No'),
		('None', 'N/A'),
	)

	checklist = models.ForeignKey(Milestone, on_delete=models.CASCADE, verbose_name=_('checklist'), related_name='checklist')
	name = models.CharField(max_length=140, verbose_name=_('item'))
	responsible =  models.CharField(max_length=3, choices=Defaults.RESPONSIBLE, verbose_name=_('responsible')) # multiselect field
	completed = models.NullBooleanField(blank=True, null=True, choices=COMP_CHOICE, verbose_name=_('is complete'))
	remarks = models.CharField(max_length=140, blank=True, verbose_name=_('comments'))
	
	def __str__(self):
		return self.checklist.description + ' - ' + self.name
