from django.conf.urls import url
from . import views

# Need to learn Regex for making the URLs
#   and how the URLs/requests allow certain records to be displayed
app_name = 'employees'
urlpatterns = [
	url(r'^$', views.list, name='list'),
	#url(r'^list/$', views.ListEmployees.as_view(), name='list'), #class based view
	# Matches numbers starting with zero and 4 or 5 digits long (employee IDs)
	url(r'^(?P<emp_id>[0-9]{4,5})/$', views.individual, name='detail'),
	url(r'^(?P<emp_id>add)/$', views.individual, name='detail'),
]