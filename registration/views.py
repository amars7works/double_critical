import urllib.request, json
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404

from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Profile, SocialLogin
from .custom_signals import post_registration_notify
from .serializers import UserProfileSerializer


class Login(APIView):
	def post(self, request, format="json"):
		username = request.data.get('username')
		password = request.data.get('password')
		user = authenticate(request, username=username, password=password)
		if user:
			login(request,user)
			return Response({"user_status":user.is_authenticated()}, status=status.HTTP_200_OK)
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
				Hi %s,

				%s is One Time Password to rest your Account

				Sincerely,
				Double Critical
				"""
			message = message.format(profile_obj.user.username.capitalize(), otp)
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


@api_view(['GET'])
def user_authentication_status(request):
	return Response(request.user.is_authenticated(), status=status.HTTP_200_OK)

class Sociallogin(APIView):
	def post(self,request,format="json"):
		email = request.data.get('email', None)
		access_token = request.data.get('accessToken', None)
		first_name = request.data.get('givenName', None)
		last_name = request.data.get('familyName', None)
		try:
			profile_obj = Profile.objects.get(user__email=email)
			if profile_obj:
				profile_obj.user.first_name=first_name
				profile_obj.user.last_name=last_name
				profile_obj.token=access_token
				profile_obj.save()
			# return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			# we have to create user and profile here
			print ('----------------------------------------------------')
			return HttpResponseRedirect("../../")
			# User.objects.create(first_name=first_name, last_name=last_name, 
			# 						email=email, token=access_token)
			# social_login_obj = SocialLogin.objects.create(**request.data)

		# URL = request.data.get('url', None)

		# with urllib.request.urlopen(URL) as url:
		# 	data = url.read().decode()
		# 	print('===========',type(data), '---------', data)

	def put(self,request,format="json"):
		provider = request.data.get('provider', None)
		name = request.data.get('name', None)
		client_id = request.data.get('client_id', None)
		refresh_token = request.data.get('refresh_token', None)
		access_token = request.data.get('access_token', None)
		try:
			social_obj = SocialLogin.objects.get(provider=provider,name=name)
			social_obj.__dict__.update(name=name)
			social_obj.__dict__.update(refresh_token=refresh_token)
			social_obj.__dict__.update(access_token=access_token)
			social_obj.save()
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			social_obj = SocialLogin.objects.create(provider=provider,name=name,client_id=client_id,
					refresh_token=refresh_token, access_token=access_token)
			return Response('user details created',status=status.HTTP_200_OK)
