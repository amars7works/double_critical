import csv
from django.db import models
from django.contrib.auth.models import User


COUNTRY_NAMES = ()
COUNTRY_CODES = ()
with open("data.csv", 'r') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		COUNTRY_NAMES += ((row[0],row[0]),)
		COUNTRY_CODES += ((row[1],row[1]),)

class State(models.Model):
	state_name =models.CharField(max_length=20)

	def __str__(self):
		return self.state_name


class Country(models.Model):
	country_code =	models.CharField(max_length=5, 
					primary_key=True, 
					choices=COUNTRY_CODES)
	country_name = models.CharField(max_length=20, 
					choices=COUNTRY_NAMES)

	def __str__(self):
		return self.country_name


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	date_of_birth = models.DateField()

	state = models.ForeignKey(State, 
				on_delete=models.CASCADE, 
				related_name='state')

	provinence = models.CharField(max_length=25, blank=True, null=True)

	country  = models.ForeignKey(Country, 
				on_delete=models.CASCADE, 
				related_name='country')

	otp = models.CharField(max_length=4, blank=True, null=True)

	terms_conditions = models.BooleanField(default=False)
	newsletter = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username
