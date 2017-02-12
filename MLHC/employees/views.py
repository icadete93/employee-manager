from rest_framework import permissions, viewsets
from employees.models import Employee
from employees.serializers import EmployeeSerializer
from django.contrib.auth.models import User
from employees.serializers import ManagerSerializer
from employees.permissions import IsOwnerOrReadOnly


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ManagerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = ManagerSerializer
