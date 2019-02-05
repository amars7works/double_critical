from django.db import models
from django.contrib.auth.models import User


class State(models.Model):
	state_name =models.CharField(max_length=20)

	def __str__(self):
		return self.state_name


class Country(models.Model):
	country_code =	models.CharField(max_length=5)
	country_name = models.CharField(max_length=20)

	def __str__(self):
		return self.country_code


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	date_of_birth = models.DateField()

	state = models.ForeignKey(State, 
				related_name='state')

	provinence = models.CharField(max_length=25, blank=True, null=True)

	country  = models.ForeignKey(Country, 
				related_name='country')

	otp = models.CharField(max_length=4, blank=True, null=True)

	terms_conditions = models.BooleanField(default=False)
	newsletter = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	def __str__(self):
		return self.user.username
