from rest_framework import serializers
from employees.models import Employee
from django.contrib.auth.models import User


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:

        model = Employee

        fields = (
            'id', 'username', 'first_name', 'last_name', 'middle_initial',
            'date_created', 'date_modified', 'active', 'personal_email',
            'group_email', 'direct_phone_number', 'cell_phone_number',
            'home_phone_number', 'supervisor', 'manager', 'division',
            'office', 'job_title', 'security_level', 'owner'
        )
        owner = serializers.ReadOnlyField(source='owner.username')


class ManagerSerializer(serializers.HyperlinkedModelSerializer):
    employees = serializers.HyperlinkedRelatedField(
        many=True, view_name='employee-detail', read_only=True
    )

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'employees', 'first_name', 'last_name',
                  'email', 'is_staff', 'is_active', 'is_superuser')
