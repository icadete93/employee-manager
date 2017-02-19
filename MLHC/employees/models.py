from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

DIV_CHOICES = (
    ('NIT', 'NIT'),
    ('DEF', 'DEF'),
    ('GHI', 'GHI'),
    ('JKL', 'JKL'),
)
OFFICE_CHOICES = (
    ('2301', '2301'),
    ('2302', '2302'),
    ('2303', '2303'),
    ('4999', '4999'),
)
JOB_TITLES = (
    ('EO', 'Escrow Officer'),
    ('TO', 'Title Officer'),
)
SECURITY_LEVELS = (
    ('S', 'Supervisor'),
    ('M', 'Manager'),
    ('E', 'Employee')
)


class Employee(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    '''
    last_name = models.CharField(
        max_length=20, verbose_name='Last Name'
    )
    first_name = models.CharField(
        max_length=20, verbose_name='First Name'
    )
    '''
    middle_initial = models.CharField(
        max_length=1, blank=True, default='', verbose_name='MI'
    )
    supervisor = models.CharField(
        max_length=40, blank=True, default='supervisor'
    )
    division = models.CharField(
        max_length=3, choices=DIV_CHOICES, default='NIT'
    )
    office = models.CharField(
        max_length=4, choices=OFFICE_CHOICES, default='2301'
    )
    date_created = models.DateField(
        auto_now_add=True
    )
    date_modified = models.DateField(
        auto_now=True
    )
    job_title = models.CharField(
        max_length=3, choices=JOB_TITLES, default='EO'
    )
    active = models.BooleanField(
        default=True
    )
    group_email = models.EmailField(
        default='group@example.com', verbose_name='Group Email'
    )
    direct_phone_number = models.CharField(
        max_length=12, blank=True, default='', verbose_name='Direct Phone Number'
    )
    cell_phone_number = models.CharField(
        max_length=12, blank=True, default='', verbose_name='Cell Phone Number'
    )
    home_phone_number = models.CharField(
        max_length=12, blank=True, default='', verbose_name='Home Phone Number'
    )
    security_level = models.CharField(
        max_length=1, choices=SECURITY_LEVELS, default='E',
        verbose_name='Security Level'
    )
    manager = models.CharField(
        max_length=40, blank=True, default='manager'
    )
