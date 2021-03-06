from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'overtime'
urlpatterns = [
	url(r'^add/$', views.add_overtime, name='add'),
	url(r'^request/$', views.overtimerequest, name='requestform'),
	#url(r'^list/(?P<page>[0-9]+)/$', login_required(views.OvertimeListView.as_view()), name='list'),
	url(r'^list/(?P<page>[0-9]+)/$', views.overtime_list, name='list'),
	url(r'^list/(?P<page>[0-9]+)/add-actual-hours/$', views.add_actual_hours, name='actualhours'), 
]