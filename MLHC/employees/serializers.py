from rest_framework import serializers
from employees.models import Employee
from django.contrib.auth.models import User


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = (
            'middle_initial',
            'date_created', 'date_modified', 'active',
            'group_email', 'direct_phone_number', 'cell_phone_number',
            'home_phone_number', 'supervisor', 'manager', 'division',
            'office', 'job_title', 'security_level',
        )


class UserSerializer(serializers.ModelSerializer):

    employee = EmployeeSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'employee')

    def create(self, validated_data):
        employee_data = validated_data.pop('employee')
        user = User.objects.create(**validated_data)
        Employee.objects.create(user=user, **employee_data)
        return user

    def update(self, instance, validated_data):
        employee_data = validated_data.pop('employee')

        employee = instance.employee

        instance.username = validated_data.get('username', 'instance.username')
        instance.email = validated_data.get('email', 'instance.email')
        instance.first_name = validated_data.get('first_name', 'instance.first_name')
        instance.save()

        employee.division = employee_data.get(
            'division',
            employee.division
        )
        employee.office = employee_data.get(
            'office',
            employee.office
        )

        employee.save()

        return instance
