from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from employees.models import Employee


"""
@receiver(post_save, sender=User)
def create_employee(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_employee(sender, instance, **kwargs):
    instance.employee.save()
"""


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, signal, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
