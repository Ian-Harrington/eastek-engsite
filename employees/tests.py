from django.test import TestCase

from .models import Employee

def create_employee(pk, name='DEFNAME', english_name='Default Name', position='ENG', is_active=True, is_leader=False, team='MECH', leader='', email='default.name@eastek-intl.com', join_date='2016-01-20',ret_date='', account=''):
	# could just create a test suite of users in a json fixture
	Employee.objects.create(

	)

class EmployeeModelTests(TestCase):
	"""tests for the Employee model"""
	# ===== Test Fields =====
	def test_Employee_emp_id(self):
		emp = Employee.objects.all()[0]
		field = emp._meta.get_field('emp_id')
		self.assertEqual(field.verbose_name, 'Employee ID')
		self.assertEqual(field.max_length, 5)
	def test_Employee_name(self):
		emp = Employee.objects.all()[0]
		field = emp._meta.get_field('name')
		self.assertEqual(field.verbose_name, 'Name')
		self.assertEqual(field.max_length, 25)
	def test_Employee_english_name(self):
		emp = Employee.objects.all()[0]
		field = emp._meta.get_field('english_name')
		self.assertEqual(field.verbose_name, 'English name')
		self.assertEqual(field.max_length, 40)
	def test_Employee_position(self):
		emp = Employee.objects.all()[0]
		field = emp._meta.get_field('position')
		self.assertEqual(field.verbose_name, 'Position')
		self.assertEqual(field.max_length, 3)
		self.assertEqual(field.choices, Employee.POSTIONS)
	def test_Employee_is_active(self):
		emp = Employee.objects.all()[0]
		field = emp._meta.get_field('is_active')
		self.assertEqual(field.verbose_name, 'Employed') # Is active')
	def test_Employee_is_leader(self):
		emp = Employee.objects.all()[0]
		field = emp._meta.get_field('is_leader')
		self.assertEqual(field.verbose_name, 'Is leader')
	def test_Employee_team(self):
		emp = Employee.objects.all()[0]
		field = emp._meta.get_field('team')
		self.assertEqual(field.verbose_name, 'Team')
		self.assertEqual(field.max_length, 3)
		self.assertEqual(field.choices, Employee.TEAMS)
	def test_Employee_leader(self):
		emp = Employee.objects.all()[0]
		field = emp._meta.get_field('leader')
		self.assertEqual(field.verbose_name, 'Leader')
	def test_Employee_email(self):
		emp = Employee.objects.all()[0]
		field = emp._meta.get_field('email')
		self.assertEqual(field.verbose_name, 'Email')
	def test_Employee_join_date(self):
		emp = Employee.objects.all()[0]
		field = emp._meta.get_field('join_date')
		self.assertEqual(field.verbose_name, 'Join date')
	def test_Employee_ret_date(self):
		emp = Employee.objects.all()[0]
		field = emp._meta.get_field('ret_date')
		self.assertEqual(field.verbose_name, 'Retire date')
	def test_Employee_account(self):
		emp = Employee.objects.all()[0]
		field = emp._meta.get_field('account')
		self.assertEqual(field.verbose_name, 'User account')
	# =======================

	def test_Employee_object_name(self):
		pass

	def test_Employee_validate_email(self):
		pass

	def test_Employee_validate_leader(self):
		pass

	def test_Employee_get_leaders(self):
		pass

	def test_Employees_has_user(self):
		pass

	def test_Employees_generate_user(self):
		pass

class ListViewTests(TestCase):
	"""docstring for ListViewTests"""
	# some setup for consistent test environment
	#   don't know how to load/clear fixtures
	def setUpTestData():
		pass

	# ===== First two tests require different user conditions (0 or 1 users) =====
	def test_list_view_no_employees(self):
		"""returns an empty table and text notifying user"""
		response = self.client.get(reverse('employees:list'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No employees found") # whatever the response is
		self.assertQuerysetEqual(response.context['emps'], [])

	def test_list_view_one_employee(self):
		"""returns the single employee available"""
		response = self.client.get(reverse('employees:list'))
		self.assertEqual(response.status_code, 200)
		# below should be modified with the one employee
		self.assertContains(response, "") 
		self.assertQuerysetEqual(response.context['emps'], Employee.objects.all())
	# ============================================================================

	def test_list_view_multiple_employee(self):
		"""displays multiple employees"""
		response = self.client.get(reverse('employees:list'))
		self.assertEqual(response.status_code, 200)
		# below should be modified with the multiple employees
		for emp in Employee.objects.all():
			self.assertContains(response, emp.emp_id) 
			self.assertContains(response, emp.name) 
			self.assertContains(response, emp.english_name) 
			self.assertContains(response, emp.email)
		self.assertQuerysetEqual(response.context['emps'], Employee.objects.all())

	def test_list_view_filtered_returns_none(self):
		"""only displays employees with the specified leader"""
		response = self.client.get(reverse('employees:list'))
		self.assertEqual(response.status_code, 200)
		# below should be modified with the multiple employees
		self.assertContains(response, "No employees found") 
		self.assertQuerysetEqual(response.context['emps'], [])

	def test_list_view_filtered_position(self):
		"""only displays employees with the specified position"""
		response = self.client.get(reverse('employees:list', kwargs={'position': 'ENG'}))
		self.assertEqual(response.status_code, 200)
		# below should be modified with the multiple employees
		self.assertContains(response, "Engineer")
		# assert the not contains 
		self.assertQuerysetEqual(response.context['emps'], Employee.objects.filter(position='ENG'))

	def test_list_view_filtered_team(self):
		"""only displays employees with the specified team"""
		response = self.client.get(reverse('employees:list', kwargs={'team': 'MECH'}))
		self.assertEqual(response.status_code, 200)
		# below should be modified with the multiple employees
		self.assertContains(response, "Mechanical") 
		# assert the not contains 
		self.assertQuerysetEqual(response.context['emps'], Employee.objects.filter(team='MECH'))

	def test_list_view_filtered_leader(self):
		"""only displays employees with the specified leader"""
		response = self.client.get(reverse('employees:list', kwargs={'leader': ''}))
		self.assertEqual(response.status_code, 200)
		# below should be modified with the multiple employees
		self.assertContains(response, "") 
		# this is a weird one, I don't know what to do (subsequent ones are bad too)
		# assert the not contains 
		self.assertQuerysetEqual(response.context['emps'], Employee.objects.filter(leader=))

	def test_list_view_filtered_position_and_leader(self):
		"""only displays employees with the specified leader"""
		response = self.client.get(reverse('employees:list', kwargs={'position': 'ENG', 'leader': ''}))
		self.assertEqual(response.status_code, 200)
		# below should be modified with the multiple employees
		self.assertContains(response, "") 
		self.assertQuerysetEqual(response.context['emps'], Employee.objects.filter(position='ENG').filter(leader=))

	def test_list_view_filtered_position_and_team(self):
		"""only displays employees with the specified leader"""
		response = self.client.get(reverse('employees:list', kwargs={'position': 'ENG', 'team': 'MECH'}))
		self.assertEqual(response.status_code, 200)
		# below should be modified with the multiple employees
		self.assertContains(response, "") 
		self.assertQuerysetEqual(response.context['emps'], Employee.objects.filter(position='ENG').filter(team='MECH'))

	def test_list_view_filtered_leader_and team(self):
		"""only displays employees with the specified leader"""
		response = self.client.get(reverse('employees:list', kwargs={'leader': '', 'team': 'MECH'}))
		self.assertEqual(response.status_code, 200)
		# below should be modified with the multiple employees
		self.assertContains(response, "") 
		self.assertQuerysetEqual(response.context['emps'], Employee.objects.filter(leader=).filter(team='MECH'))

	def test_list_view_filtered_position_and_leader_and team(self):
		"""only displays employees with the specified leader"""
		response = self.client.get(reverse('employees:list', kwargs={'position': 'ENG', 'leader': , 'team': 'MECH'}))
		self.assertEqual(response.status_code, 200)
		# below should be modified with the multiple employees
		self.assertContains(response, "") 
		self.assertQuerysetEqual(response.context['emps'], Employee.objects.filter(position='ENG').filter(leader=).filter(team='MECH'))
	

class DetailViewTests(TestCase):
	"""docstring for DetailViewTests"""
	def test_detail_view_GET_404(self):
		response = self.client.get(reverse('employees:detail', kwargs={'arg': '09999'}))
		self.assertEqual(response.status_code, 404)

	def test_detail_view_GET_Employee(self):
		pass
		
	def test_detail_view_GET_add_Employee(self):
		pass

	def test_detail_view_POST_add_Employee(self):
		pass

	def test_detail_view_POST_edit_Employee(self):
		pass