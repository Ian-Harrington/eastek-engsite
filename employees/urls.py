from django.conf.urls import url
from . import views

# Need to learn Regex for making the URLs
#   and how the URLs/requests allow certain records to be displayed
app_name = 'employees'
urlpatterns = [
	url(r'^$', views.list, name='list'),
	url(r'^(?P<emp_id>add|[0-9]{4,5})/$', views.individual, name='detail'),
	#url(r'^(?P<emp_id>add)/$', views.individual, name='detail'),
	url(r'^(?P<emp_id>[0-9]{4,5})/create_account/$', views.generate_account, name='genaccount'),
]