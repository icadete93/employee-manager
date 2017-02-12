from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from employees import views

router = DefaultRouter()
router.register(r'employees', views.EmployeeViewSet)
router.register(r'managers', views.ManagerViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
