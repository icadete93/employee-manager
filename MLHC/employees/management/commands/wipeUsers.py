from django.core.management.base import BaseCommand
from employees.models import *
from django.contrib.auth.models import User

class Command(BaseCommand):
	def handle(self, **options):
		i = 2
		maxID = EmployeeUser.objects.latest('id').id
		print("Highest id is",maxID)
		while(i<maxID):
			if(EmployeeUser.objects.filter(id=i).count() != 0):
				e = EmployeeUser.objects.get(id=i)
				print("DELETING ID",i,"USERNAME:",e.username)
				e.delete()
			i += 1
