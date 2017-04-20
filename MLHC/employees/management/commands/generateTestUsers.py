from django.core.management.base import BaseCommand
from employees.models import *
from django.contrib.auth.models import User

class Command(BaseCommand):
	def handle(self, **options):
		for i in range(10):
			uname = "testEmployee"+str(i)
			self.newEmployee(uname,uname+"@gmail.com","E","epauley")

	def newEmployee(self,username,email,secLevel,manager):
		e = EmployeeUser.objects._create_user(username, email, secLevel, "1" ,employee__manager= manager)
		e.employee.manager = manager
		e.employee.save()
		e.save()
		
		
