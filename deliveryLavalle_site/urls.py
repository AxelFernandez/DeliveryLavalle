"""deliveryLavalle_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import logout
from django.urls import path, include

from core import urls as core_urls
from api import urls as api_urls
from deliveryLavalle_site import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('logout/', views.logout_view, name='logout'),
    path('tutorial_meli_link/', views.tutorial_meli_link, name='tutorial-meli-link'),
    path('terminosycondiciones/', views.term_and_conditions, name='term-and-conditions'),
    path('', include(core_urls)),
    path('api/', include(api_urls)),

]