from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	date_of_birth = models.DateField()

	state =models.CharField(max_length=20)
	country_code =models.CharField(max_length=20)
	country_name = models.CharField(max_length=5)

	terms_conditions = models.BooleanField(default=False)
	newsletter = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username
