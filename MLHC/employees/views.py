from rest_framework import (
    status, permissions, viewsets
)
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from employees.models import EmployeeUser
from employees.serializers import (
    EmployeeSerializer, CreateUserSerializer,
    ChangePasswordSerializer, UpdateUserSerializer
)
from .permissions import (
    ManagerPermission, IsOwner, PasswordChangePermission
)


class UserViewSet(viewsets.ModelViewSet):

    queryset = EmployeeUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field = 'username'

    def get_serializer_class(self):
        if self.request.method == 'POST' and (self.request.user.security_level == 'M' or self.request.user.security_level == 'S'):
            return CreateUserSerializer
        else:
            return UpdateUserSerializer


class UserList(APIView):

    permission_classes = (permissions.IsAuthenticated, ManagerPermission,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'employees/user_list.html'

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def get(self, request, format=None):
        queryset = EmployeeUser.objects.filter(employee__manager=self.get_object().username)
        return Response({'employees': queryset})


class ChangePasswordView(UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = EmployeeUser
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,
        PasswordChangePermission,
    )
    lookup_field = 'username'

    # def get_serializer_class(self):
    #     if self.get_object().username in self.request.get_full_path():
    #         return ChangePasswordSerializer
    #     else:
    #         return UpdateUserSerializer

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
