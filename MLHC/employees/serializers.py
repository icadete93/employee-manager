from rest_framework import serializers
from employees.models import Employee
from django.contrib.auth import update_session_auth_hash
from .models import EmployeeUser


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = (
            'middle_initial',
            'date_created',
            'date_modified',
            'active',
            'group_email',
            'direct_phone_number',
            'cell_phone_number',
            'home_phone_number',
            'supervisor',
            'manager',
            'division',
            'office',
            'job_title',
        )


class CreateUserSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = EmployeeUser
        fields = (
          'id',
          'first_name',
          'last_name',
          'username',
          'email',
          'password',
          'security_level',
          'employee',
        )

    def create(self, validated_data):
        employee_data = validated_data.pop('employee')
        user = EmployeeUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Employee.objects.create(user=user, **employee_data)
        return user

    def update(self, instance, validated_data):

        employee = instance.employee

        instance.username = validated_data.get(
            'username', 'instance.username'
        )
        instance.email = validated_data.get(
            'email', 'instance.email'
        )
        instance.last_name = validated_data.get(
            'last_name', 'instance.last_name'
        )
        instance.first_name = validated_data.get(
            'first_name', 'instance.first_name'
        )
        instance.security_level = validated_data.get(
            'security_level', 'instance.security_level'
        )
        instance.set_password(validated_data['password'])
        instance.save()

        employee_data = validated_data.pop('employee')

        employee.division = employee_data.get(
            'division',
            employee.division
        )
        employee.office = employee_data.get(
            'office',
            employee.office
        )
        employee.manager = employee_data.get(
            'manager',
            employee.manager
        )
        employee.supervisor = employee_data.get(
            'supervisor',
            employee.supervisor
        )
        employee.group_email = employee_data.get(
            'group_email',
            employee.group_email
        )
        employee.direct_phone_number = employee_data.get(
            'direct_phone_number',
            employee.direct_phone_number
        )
        employee.cell_phone_number = employee_data.get(
            'cell_phone_number',
            employee.cell_phone_number
        )
        employee.home_phone_number = employee_data.get(
            'home_phone_number',
            employee.home_phone_number
        )
        employee.job_title = employee_data.get(
            'job_title',
            employee.job_title
        )
        employee.active = employee_data.get(
            'active',
            employee.active
        )
        employee.date_created = employee_data.get(
            'date_created',
            employee.date_created
        )
        employee.date_modified = employee_data.get(
            'date_modified',
            employee.date_modified
        )
        employee.save()

        update_session_auth_hash(self.context.get('request'), instance)
        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()

    class Meta:
        model = EmployeeUser
        fields = (
          'id',
          'first_name',
          'last_name',
          'username',
          'email',
          'security_level',
          'employee',
        )
        extra_kwargs = {
            'employee': {'read_only': True}
        }

    def update(self, instance, validated_data):

        employee = instance.employee

        instance.username = validated_data.get(
            'username', 'instance.username'
        )
        instance.email = validated_data.get(
            'email', 'instance.email'
        )
        instance.last_name = validated_data.get(
            'last_name', 'instance.last_name'
        )
        instance.first_name = validated_data.get(
            'first_name', 'instance.first_name'
        )
        instance.security_level = validated_data.get(
            'security_level', 'instance.security_level'
        )
        instance.save()

        employee_data = validated_data.pop('employee')

        employee.division = employee_data.get(
            'division',
            employee.division
        )
        employee.office = employee_data.get(
            'office',
            employee.office
        )
        employee.manager = employee_data.get(
            'manager',
            employee.manager
        )
        employee.supervisor = employee_data.get(
            'supervisor',
            employee.supervisor
        )
        employee.group_email = employee_data.get(
            'group_email',
            employee.group_email
        )
        employee.direct_phone_number = employee_data.get(
            'direct_phone_number',
            employee.direct_phone_number
        )
        employee.cell_phone_number = employee_data.get(
            'cell_phone_number',
            employee.cell_phone_number
        )
        employee.home_phone_number = employee_data.get(
            'home_phone_number',
            employee.home_phone_number
        )
        employee.job_title = employee_data.get(
            'job_title',
            employee.job_title
        )
        employee.active = employee_data.get(
            'active',
            employee.active
        )
        employee.date_created = employee_data.get(
            'date_created',
            employee.date_created
        )
        employee.date_modified = employee_data.get(
            'date_modified',
            employee.date_modified
        )
        employee.save()
        update_session_auth_hash(self.context.get('request'), instance)

        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, style={'input_type': 'password'})
