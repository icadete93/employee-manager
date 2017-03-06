from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from employees import views

router = DefaultRouter()
router.register(r'employees', views.EmployeeViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^users/(?P<pk>[0-9]+)/change-password/$', views.ChangePasswordView.as_view()),
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/$', csrf_exempt(obtain_jwt_token))
]
