from rest_framework import serializers
from employees.models import Employee
from employees import models
from django.contrib.auth.models import User
from .models import EmployeeUser


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = (
            'id', 'middle_initial', 'date_created',
            'date_modified', 'active', 'group_email', 'direct_phone_number',
            'cell_phone_number', 'home_phone_number', 'supervisor',
            'manager', 'division', 'office', 'job_title', 'security_level',
        )
    '''
    def create(self, validated_data):

        user = self.context['request'].user
        return models.Employee.objects.create(user=user, **validated_data)
    '''


class UserSerializer(serializers.ModelSerializer):

    employee = EmployeeSerializer()

    class Meta:
        model = EmployeeUser
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name', 'employee',
                  )

    def create(self, validated_data):

        employee_data = validated_data.pop('employee')
        user = EmployeeUser.objects.create(**validated_data)
        '''
        user = EmployeeUser(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],

        )
        '''
        # if validated_data['password']:
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
        instance.first_name = validated_data.get(
            'first_name', 'instance.first_name'
        )
        instance.last_name = validated_data.get(
            'last_name', 'instance.last_name'
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
        employee.security_level = employee_data.get(
            'security_level',
            employee.security_level
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

        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
