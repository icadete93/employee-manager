"""MLHC URL Configuration

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
from django.conf import settings
from employees import views
from rest_framework.routers import SimpleRouter
from django.contrib.auth import views as djangoview
template_name = {'template_name': 'rest_framework/login.html'}

router = SimpleRouter()
router.register(r'users', views.UserViewSet, base_name='user')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', djangoview.login, template_name, name='login',),
    url(r'^logout/$', djangoview.logout, template_name, name='logout'),
    url(r'^', include(router.urls)),
    url(r'^', include('employees.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
