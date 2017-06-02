"""EngSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView

from users import views as user_views

#from .views import HomeView

urlpatterns = [
    url(r'^$', login_required(TemplateView.as_view(template_name='home.html')), name='landing'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    url(r'^WIP/$', login_required(TemplateView.as_view(template_name='WIP.html')), name='WIP'),
    url(r'^overtime/', include('overtime.urls')),
    url(r'^user/', include('users.urls')),
    url(r'^employees/', include('employees.urls')),
    url(r'^projects/', include('projects.urls')),
    url(r'^admin/', admin.site.urls)
]