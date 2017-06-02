from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from . import views

app_name = 'overtime'
urlpatterns = [
	url(r'^add/$', views.add_overtime, name='add'),
	url(r'^request/$', views.overtimerequest, name='requestform'),
	url(r'^list/(?P<page>[0-9]+)/$', login_required(views.OvertimeListView.as_view()), name='list'), 
	# ===== Temporary Project Info =====
	#url(r'^addproject/$', views.AddProjectView.as_view(), name='addproject'),
	#url(r'^editproject/$', views.EditProjectView.as_view(), name='editproject'),
	#url(r'^listproject/$', views.ListProjectView.as_view(), name='listproject'),
]