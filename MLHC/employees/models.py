import uuid
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token

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


class EmployeeUserManager(BaseUserManager):
    def create_user(self, username, email, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, last_name, password, **extra_fields):
        user = self.create_user(username, email, last_name, password=password, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user


class EmployeeUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = EmployeeUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'last_name']

    def get_full_name(self):
        username = self.clean(self.username)
        return username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.email

    def get_email(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name_plural = "Users"


class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

    def username(self):
        return self.user.get_username()
    username = property(username)

    def email(self):
        return self.user.email
    email = property(email)

    def last_name(self):
        return self.user.last_name
    last_name = property(last_name)

    def first_name(self):
        return self.user.first_name
    first_name = property(first_name)

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

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_employee(sender, created, instance, **kwargs):
        if created:
            employee = Employee(user=instance)
            employee.save()

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, signal, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)
