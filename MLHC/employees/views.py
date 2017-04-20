from rest_framework import (
    status, permissions, viewsets
)
from django.contrib.auth import get_user_model
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

# Password Reset Email Imports #
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from config.settings import DEFAULT_FROM_EMAIL
from django.views.generic import *
from .forms import PasswordResetRequestForm, SetPasswordForm
from django.contrib import messages
from django.db.models.query_utils import Q
##########################################


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


class ResetPasswordRequestView(FormView):
    template_name = "employees/test_template.html"
    success_url = '/reset_password/'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):

        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email_or_username"]
        if self.validate_email_address(data) is True:
            associated_users = EmployeeUser.objects.filter(Q(email=data) | Q(username=data))
            if associated_users.exists():
                for user in associated_users:
                        c = {
                            'email': user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': 'your site',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                        }
                        subject_template_name = 'registration/password_reset_subject.txt'
                        # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                        email_template_name = 'registration/password_reset_email.html'
                        # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                        subject = loader.render_to_string(subject_template_name, c)
                        # Email subject *must not* contain newlines
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'No user is associated with this email address')
            return result
        else:
            associated_users = EmployeeUser.objects.filter(username=data)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': 'localhost:8000',  # or your domain
                        'site_name': 'group 131',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    subject_template_name = 'registration/password_reset_subject.txt'
                    email_template_name = 'registration/password_reset_email.html'
                    subject = loader.render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                    result = self.form_valid(form)
                    messages.success(request, 'Email has been sent to ' + data + "'s email address. Please check your inbox for a link to reset your password.")
                    return result
                result = self.form_invalid(form)
                messages.error(request, 'This username does not exist in the system.')
                return result
            messages.error(request, 'Invalid Input')
            return self.form_invalid(form)


class PasswordResetConfirmView(FormView):
    template_name = "employees/test_template.html"
    success_url = '/login'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(
                    request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(
                request, 'The reset password link is no longer valid.')
            return self.form_invalid(form)
