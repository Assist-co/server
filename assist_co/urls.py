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
from assist_co_server.views import *

router = DefaultRouter(trailing_slash=False)
router.register(r'^api/options/professions', ProfessionViewSet)
router.register(r'^api/options/genders', GenderViewSet)
router.register(r'^api/options/task-types', TaskTypeViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api/login$', LoginView.as_view()),
    url(r'^api/signup$', ClientSignupView.as_view()),
    url(r'^api/logout$', LogoutView.as_view()),
]