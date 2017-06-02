from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from .models import Employee
from .forms import FilterListForm, IndividualForm


@login_required
@permission_required(['employees.add_employee', 'employees.change_employee'], raise_exception=True)
def list(request):
	# Returns list of all employees (filtered by ___)
	emps = Employee.objects.all()
	form = FilterListForm()
	if request.GET: # true only when there are values for the GET attribute (request.method == 'GET')
		filters = {'team':request.GET.get('team'),
				'leader':request.GET.get('leader'),
				'position':request.GET.get('position'),
				'retired':request.GET.get('ret')=='on'}
		if filters['team'] != '':
			emps = emps.filter(team=filters['team'])
		if filters['leader'] != '':
			emps = emps.filter(leader=filters['leader'])
		if filters['position'] != '':
			emps = emps.filter(position=filters['position'])
		form = FilterListForm(filters)
	emps = emps.filter(is_active=not request.GET.get('ret')=='on')
	context = {
		'emps': emps,
		'filterform': form
	}
	return render(request, 'employees/list.html', context)


@login_required
@permission_required(['employees.add_employee', 'employees.change_employee'], raise_exception=True)
def individual(request, emp_id):
	# Returns detail view of one employee (as a form)
	# GET requests supress errors, POST requests display
	context = {}
	if request.method == 'POST':
		# validate & save data (new or edit employee)
		if Employee.objects.filter(pk=request.POST.get('emp_id')).count() == 1:
			emp = Employee.objects.get(pk=request.POST.get('emp_id'))
			form = IndividualForm(request.POST, instance=emp, initial={'user_acc': emp.has_user()}) # is this actually what is wanted? does request have presidence? what about overriding the user account field?
		else:
			form = IndividualForm(request.POST)
		if form.is_valid():
			# check against other validation methods? (email domain, etc.)
			form.save()
			context['saved'] = True
			if form.cleaned_data['user_acc']:
				emp = Employee.objects.get(pk=form.cleaned_data['emp_id'])
				emp.generate_user(supress=True)
				assert emp.account.is_active
				user = emp.account
				user.groups.add(Group.objects.get(name='default'))
				if emp.team == 'SUPP':
					user.groups.add(Group.objects.get(name='support'))
			if not form.cleaned_data['is_active'] and emp.has_user():
				emp.archive_account()
		else:
			pass
		# common context	
		context['arg'] = request.POST.get('emp_id')
	else:
		if emp_id == 'add':
		# create new blank form
			form = IndividualForm()
			context['arg'] ='add'
		else:
			emp = get_object_or_404(Employee, pk=emp_id)
			assert emp.emp_id == emp_id
			form = IndividualForm(instance=emp, initial={'user_acc': emp.has_user()})
			context['emp'] = emp
			context['arg'] = emp.emp_id
	context['indvform'] = form
	return render(request, 'employees/detail.html', context)

