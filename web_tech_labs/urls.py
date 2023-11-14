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
from labs.views import InfoView, HomeView

labs_urls = [
    # View
    path("<str:lab_name>/", views.get_lab_view_by_name, name="lab"),
    # Routes for post request handle
    path("1/", include("labs.lab1.urls")),
    path("2/", include("labs.lab2.urls")),
    path("3/", include("labs.lab3.urls")),
]

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    # path("labs/<str:lab_name>/", views.get_lab_view_by_name, name="lab"),
    path("labs/", include(labs_urls)),
    path("", include("labs.lab4.urls")),
    path("info/", InfoView.as_view()),
    path("admin/", admin.site.urls),
]
