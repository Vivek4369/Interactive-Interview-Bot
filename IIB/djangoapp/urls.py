"""djangoapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin  
from django.urls import path  
from myapp import views as user_views
from admin_app import views as admin_views
urlpatterns = [  
    path('', user_views.login),
    path('login/',user_views.login),
    path('admin/', admin.site.urls),  
    path('demo/', user_views.demo),  
    path('home/', user_views.home),
    path('features/', user_views.features),
    path('integration/', user_views.integration),
    path('resources/', user_views.resources),
    path('solutions/', user_views.solutions),
    path('registration/', user_views.registration),
    path('result/', user_views.result),
    path('dashboard/', user_views.dashboard),
    path('admin_login/',admin_views.admin_login),
    path('jobs/', user_views.jobs),
    path('about_job/', user_views.about_job),

    path('admin_demo/', admin_views.admin_demo),  
    path('admin_home/', admin_views.admin_home),
    path('admin_features/', admin_views.admin_features),
    path('admin_integration/', admin_views.admin_integration),
    path('admin_resources/', admin_views.admin_resources),
    path('admin_solutions/', admin_views.admin_solutions),
    path('admin_registration/', admin_views.admin_registration),
    path('admin_result/', admin_views.admin_result),
    path('admin_dashboard/', admin_views.admin_dashboard),
    path('new_job/', admin_views.new_job),
    path('admin_jobs/', admin_views.admin_jobs)

]  