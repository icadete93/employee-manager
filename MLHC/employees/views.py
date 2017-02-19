from rest_framework import viewsets
#from rest_framework.response import Response
from employees.models import Employee
from employees.serializers import EmployeeSerializer, UserSerializer
from django.contrib.auth.models import User


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer