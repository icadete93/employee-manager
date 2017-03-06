from rest_framework import permissions, viewsets
from employees.permissions import IsOwner, EmployeePermission
#from rest_framework.response import Response
from employees.models import Employee, EmployeeUser

from employees.serializers import (
    EmployeeSerializer, UserSerializer,
    ChangePasswordSerializer
)
from django.contrib.auth.models import User
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import UpdateAPIView


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    @detail_route(methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = EmployeeUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeePermission,)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = EmployeeUser
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success.", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
