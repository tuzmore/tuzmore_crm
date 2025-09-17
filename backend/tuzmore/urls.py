"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .import views
from django.shortcuts import render
# Swagger setup
schema_view = get_schema_view(
    openapi.Info(
        title = 'Tuzmore API',
        default_version='v1',
        description = 'Tuzmore Api documentation form CRM system',
    ),
    public=True,
    permission_classes= (permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
    path('api/', include('contacts.urls')),
    path('api/', include('teams.urls')),
    path('api/', include('deals.urls')),
    path('api/', include('tasks.urls')),
    path('api/', include('inbox.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('', views.landing_view, name='landing'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('deals/', lambda request: render(request, 'deals.html'), name='deals'),
    path('contacts/', lambda request: render(request, 'contacts.html'), name='contacts'),
    path('tasks/', lambda request: render(request, 'tasks.html'), name='tasks'),
    path('about/', views.about_view, name='about'),
    path('solutions/', views.solutions_view, name='solutions'),
    path('contact/', views.contact_us_view, name='contact'),
    path('inbox/', views.inbox_view, name='inbox'),
    path('blog/', views.blog_view, name='blog' ),





]
