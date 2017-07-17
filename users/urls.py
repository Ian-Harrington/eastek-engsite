from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'
urlpatterns = [
	#url(r'^settings/$', auth_views.PasswordChangeView.as_view(template_name='users/pwd_change.html', success_url='/'), name='settings'),
	url(r'^set-password/$', views.change_password, name='setpassword'),
	#url(r'^set-homepage/$', views.set_home_projects, name='setlinks'),
]