from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Profile
from .custom_signals import post_registration_notify
from .serializers import UserProfileSerializer

class Login(APIView):
	def post(self, request, format="json"):
		username = request.data.get('username')
		password = request.data.get('password')
		user = authenticate(request, username=username, password=password)
		if user:
			login(request,user)
			return Response({"user_status":user.is_authenticated(),
			"terms_conditions":user.profile.terms_conditions}, status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_401_UNAUTHORIZED)


class Logout(APIView):
	def get(self,request,format="json"):
		logout(request)
		return Response(status=status.HTTP_200_OK)

class UserCreate(APIView):
	def post(self, request, format="json"):
		serializer = UserProfileSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			if user:
				user = authenticate(request,
					username = request.data['username'],
					password = request.data['password']
				)
				login(request,user)
				post_registration_notify.send(
					sender = self.__class__,
					email_address = user.email,
					username = user.username
				)
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def generate_otp():
	otp = get_random_string(4, allowed_chars='0123456789')
	return otp

class ForgotPassword(APIView):
	def post(self, request, format="json"):
		email = request.data.get('email', None)
		try:
			profile_obj = Profile.objects.get(user__email=email)
			otp = profile_obj.otp
			if not otp:
				otp = generate_otp()
			profile_obj.__dict__.update(otp=otp)
			profile_obj.save()
			message = """
				Hi {},

				{} is Ont Time Password to rest your Account

				Sincerely,
				Double Critical   
				"""
			message = message.format(profile_obj.user.username, otp)
			send_mail(
				subject="One Time Password",
				message = message,
				from_email = "dealswallet.com@gmail.com",
				recipient_list = [email],
				fail_silently = True  
			)
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)


# import os
# os.environ['DJANGO_SETTINGS_MODULE'] = 'doublecritical.settings.local'

#         )
class ResetPassword(APIView):
	def post(self, request, format="json"):
		otp = request.data.get('otp', None)
		email = request.data.get('email', None)
		password = request.data.get('password', None)
		try:
			profile_obj = Profile.objects.get(user__email=email, otp=otp)
			profile_obj.__dict__.update(otp=None)
			profile_obj.save()

			user_obj = User.objects.get(email=email)
			user_obj.set_password(password)
			user_obj.save()
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

