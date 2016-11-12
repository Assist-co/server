"""assist_co URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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

from rest_framework.routers import DefaultRouter

import rest_framework_docs
from assist_co_server.views import *


urlpatterns = [
    # Add-ons
    # url(r'^docs/', include('rest_framework_docs.urls')),

    # Option urls
    url(r'^api/options/professions$', ProfessionsView.as_view()),
    url(r'^api/options/genders$', GendersView.as_view()),
    url(r'^api/options/task-types$', TaskTypesView.as_view()),

    # Auth urls
    url(r'^api/login$', LoginView.as_view()),
    url(r'^api/signup$', ClientSignupView.as_view()),
    url(r'^api/logout$', LogoutView.as_view()),

    # Client & Tasks urls
    url(r'^api/tasks$', TasksView.as_view()),
    url(r'^api/clients/(?P<id>[0-9]+)/tasks$', ClientTasksView.as_view()),
    url(r'^api/clients/(?P<client_id>[0-9]+)/tasks/(?P<id>[0-9]+)$', ClientTaskDetailView.as_view()),

    # Client urls
    url(r'^api/clients$', ClientsView.as_view()),
    url(r'^api/clients/(?P<id>[0-9]+)$', ClientDetailView.as_view()),

    # Assistant urls
    url(r'^api/assistants$', AssistantsView.as_view()),
    url(r'^api/assistants/(?P<id>[0-9]+)$', AssistantsDetailView.as_view()), 
]
