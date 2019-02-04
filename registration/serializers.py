from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import *

class UserProfileSerializer(serializers.ModelSerializer):
	username = serializers.CharField(source='user.username')
	email = serializers.EmailField(source='user.email')
	password = serializers.CharField(source='user.password',write_only=True)

	def validate_username(self,username):
	   '''
		Make a case insensitive check to determine uniqueness of username
	   '''
	   UserModel = get_user_model()
	   case_insensitive_username_field = "{}__iexact".format(UserModel.USERNAME_FIELD)
	   if (username and UserModel._default_manager.filter(
			**{case_insensitive_username_field:username}).exists()):
	   		raise serializers.ValidationError("Username already exist")
	   return username

	def validate_email(self,email):
	   '''
		Make a case insensitive check to determine uniqueness of email
	   '''
	   UserModel = get_user_model()
	   case_insensitive_email_field = "{}__iexact".format(UserModel.EMAIL_FIELD)
	   if (email and UserModel._default_manager.filter(
			**{case_insensitive_email_field:email}).exists()):
	   		raise serializers.ValidationError("Email already exist")
	   return email

	class Meta:
		model = Profile
		fields = ('id','username','email','password', 'date_of_birth',
					'state', 'country',	'terms_conditions', 'newsletter')

	def create(self,validated_data):
		user_data = validated_data.pop('user')
		user = User.objects.create_user(**user_data)
		profile = Profile.objects.create(user=user,**validated_data)
		return profile

	def update(self, instance, validated_data):
		user = instance.user
		user.email = validated_data.get('email',user.email)
		user.save()
		instance.date_of_birth = validated_data.get('date_of_birth',instance.date_of_birth)
		instance.country = validated_data.get('country', instance.country)
		instance.state = validated_data.get('state', instance.state)
		instance.newsletter = validated_data.get('newsletter', instance.newsletter)
		instance.save()
		return instance
		
