"""geodjango URL Configuration

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
from django.urls import path
from .views import CountryViewSet

urlpatterns = [
    path('countries', CountryViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'upload'
    })),
    path('countries/<str:pk>', CountryViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('countries/name/<str:pk>', CountryViewSet.as_view({
        'get': 'matching_names'
    })),
    path('countries/intersect/<str:pk>', CountryViewSet.as_view({
        'get': 'intersecting'
    }))]

