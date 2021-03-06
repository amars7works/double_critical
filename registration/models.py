from django.db import models
from django.contrib.auth.models import User



class Country(models.Model):
	country_code =	models.CharField(max_length=5)
	country_name = models.CharField(max_length=50)

	def __str__(self):
		return self.country_name


class State(models.Model):
	state_name = models.CharField(max_length=20)

	def __str__(self):
		return self.state_name


class Profile(models.Model):
	GENDER_CHOICE = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other")
    )

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	date_of_birth = models.DateField(blank=True, null=True)
	gender = models.CharField(default="Male", max_length=10, choices=GENDER_CHOICE)
	state = models.CharField(max_length=30)
	provinence = models.CharField(max_length=25, blank=True, null=True)
	country = models.CharField(max_length=5)
	otp = models.CharField(max_length=4, blank=True, null=True)
	terms_conditions = models.BooleanField(default=False)
	newsletter = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)
	avatar = models.ImageField(upload_to='uploads/',null = True)

	def __str__(self):
		return self.user.username

class SocialLogin(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	google_client_id = models.CharField(max_length=250,null=True)
	facebook_client_id = models.CharField(max_length=250,null=True)
	google_refresh_token = models.TextField(blank=True,null=True)
	facebook_refresh_token = models.TextField(blank=True,null=True)
	google_access_token = models.TextField(blank=True,null=True)
	facebook_access_token = models.TextField(blank=True,null=True)
	google_id_token = models.TextField(blank=True,null=True)
	access_token_expiry = models.DateTimeField(blank=True,null=True)

	def __str__(self):
		return str(self.user)
