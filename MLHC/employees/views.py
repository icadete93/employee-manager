from rest_framework import (
    status, permissions, viewsets
)
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from employees.models import EmployeeUser
from employees.serializers import (
    EmployeeSerializer, CreateUserSerializer,
    ChangePasswordSerializer, UpdateUserSerializer
)


class UserViewSet(viewsets.ModelViewSet):

    queryset = EmployeeUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'username'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserSerializer
        else:
            return UpdateUserSerializer

    @list_route()
    def managed_users(self, request):
        managed_users = EmployeeUser.objects.filter(employee__manager=self.request.user.username)

        page = self.paginate_queryset(managed_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(managed_users, many=True)
        return Response(serializer.data)


class UserList(APIView):

    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)
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
