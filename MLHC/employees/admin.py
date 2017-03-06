from employees import models
from employees.models import EmployeeUser
from employees.models import Employee

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db.models import Count


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = EmployeeUser
        fields = ('username', 'email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EmployeeCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ()

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(EmployeeCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = EmployeeUser
        fields = ('username', 'email', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class EmployeeChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Employee
        fields = ('user',)

    def username(self, obj):
        return obj.username

    def clean_password(self):
        return self.initial["password"]


class EmployeeUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_admin', 'column_employee_count')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    def get_queryset(self, request):
        return models.EmployeeUser.objects.annotate(employee_count=Count('employee'))

    def column_employee_count(self, instance):
        return instance.employee_count

    column_employee_count.short_description = 'employee_count'
    column_employee_count.admin_order_field = 'employee_count'


class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeChangeForm
    add_form = EmployeeCreationForm
    list_display = ('user', 'user_get_username')
    search_fields = ('user__email',)
    ordering = ('user',)

    def user_get_username(self, obj):
        return obj.user.get_username()

admin.site.register(models.Employee, EmployeeAdmin)
admin.site.register(EmployeeUser, EmployeeUserAdmin)
admin.site.unregister(Group)