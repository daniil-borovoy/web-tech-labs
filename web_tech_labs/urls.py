"""
URL configuration for web_tech_labs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include

from labs import views

urlpatterns = [
    path('', views.index, name='home'),
    path('labs/<str:lab_number>/', views.render_lab, name='lab'),
    path('labs/2/', include('labs.lab2.urls')),
    path('labs/3/', include('labs.lab3.urls')),
    path('info/', views.info),
    path('admin/', admin.site.urls),
]
