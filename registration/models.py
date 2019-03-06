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
		return self.country_name


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

	token = models.CharField(max_length=50, blank=True, null=True)

	newsletter = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	def __str__(self):
		return self.user.username

class SocialLogin(models.Model):
	# PROVIDER = (
	# 	('facebook','FACEBOOK'),
	# 	('google','GOOGLE')
	# 	)
	# provider = models.CharField(
	# 			max_length=10,
	# 			choices=PROVIDER,
	# 			default=None
	# 			)
	user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
	name = models.CharField(max_length=35,blank=True,null=True)
	family_name = models.CharField(max_length=35,blank=True,null=True)
	given_name = models.CharField(max_length=35,blank=True,null=True)
	birthdate = models.DateTimeField(blank=True,null=True)
	client_id = models.CharField(max_length=250,null=True)
	refresh_token = models.TextField(blank=True,null=True)
	google_access_token = models.TextField(blank=True,null=True)
	facebook_access_token = models.TextField(blank=True,null=True)
	id_token = models.TextField(blank=True,null=True)
	access_token_expiration_date = models.DateTimeField()

	def __str__(self):
		return str(self.name)

	# class Meta:
	# 	unique_together = ('provider', 'name')
