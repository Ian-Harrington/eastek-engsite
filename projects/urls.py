from django.conf.urls import url
from django.contrib.auth.decorators import login_required
#from django.views.generic import DetailView
from . import views

app_name = 'projects'
urlpatterns = [
	url(r'^$', login_required(views.ProjectListView.as_view()), name='projectlist'),
	url(r'^(?P<pid>[0-9]+)/$', views.project_page, name='dashboard'),
	url(r'^(?P<pid>[0-9]+)/status_update/$', views.change_project_status, name='statusupdate'),
	url(r'^(?P<pid>[0-9]+)/join_project/$', views.add_self_to_project, name='joinproject'),
	url(r'^add/$', views.add_project, name='addproject'),
	#url(r'^(?P<pid>[0-9]+)/milestones/$', views.project_milestones, name='milestones'),
	#url(r'^(?P<pid>[0-9]+)/milestones/completion_status$', views.change_milestone_completion, name='milestonecompletion'),
	url(r'^(?P<pid>[0-9]+)/updates/$', views.project_updates, name='updates'),
	url(r'^(?P<pid>[0-9]+)/updates/add/$', views.add_update, name='addupdate'),
	url(r'^(?P<pid>[0-9]+)/gate/(?P<gate>[12345])/$', views.complete_checklist, name='checklist'),
	url(r'^customers/$', views.CustomerListView.as_view(), name='customers'),
	url(r'^customers/add_new_customer/$', views.add_customer, name='addcustomer'),
]