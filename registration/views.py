import urllib.request, json
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404

from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.shortcuts import redirect
import ast

from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Profile, SocialLogin
from game.models import *
from dc.models import FollowUser
from .custom_signals import post_registration_notify
from .serializers import UserProfileSerializer,UserSerializer,GameCollectionSerializer
from django.forms.models import model_to_dict

class Login(APIView):
	def post(self, request, format="json"):
		username = request.data.get('username')
		password = request.data.get('password')
		print (username, password)
		user = authenticate(request, username=username, password=password)
		print (user, '==========================')
		if user:
			login(request,user)
			return Response({"user_status":user.is_authenticated(), "user_id":user.id}, 
						status=status.HTTP_200_OK)
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

				{}is One Time Password to rest your Account

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
	"""
	Parameters: email, otp
	try: Validating the user enterd otp based on the randomly generated otp
	which was send to user email
	Retunrn: status

	"""

	def get(self,request, format = "json"):
		otp = request.data.get('otp', None)
		email = request.data.get('email', None)
		try:
			profile_obj = Profile.objects.get(user__email=email, otp=otp)
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

	"""
	Parameters: email, password
	try: password saves into database then otp will be none 
	Retunrn: status
	
	"""
	def post(self, request, format="json"):
		email = request.data.get('email', None)
		password = request.data.get('password', None)
		try:
			profile_obj = Profile.objects.get(user__email=email)
			user_obj = User.objects.get(email=email)
			user_obj.set_password(password)
			user_obj.save()
			profile_obj.__dict__.update(otp=None)
			profile_obj.save()
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_authentication_status(request):
	return Response({"user_status":request.user.is_authenticated(), 
					"user_id":user.id}, status=status.HTTP_200_OK)

class Googlelogin(APIView):
	def post(self,request,format="json"):
		provider = request.data.get('provider', None)

		email = request.data.get('email', None)
		access_token = request.data.get('access_token', None)
		first_name = request.data.get('given_name', None)
		last_name = request.data.get('family_name', None)
		username = request.data.get('username', None)

		client_id = request.data.get('client_id', None)
		refresh_token = request.data.get('refresh_token', None)
		id_token = request.data.get('id_token', None)
		access_token_expiry = request.data.get('access_token_expiry', None)

		try:
			user_obj = User.objects.get(email=email)

			profile_obj = Profile.objects.get(user=user_obj)
			if profile_obj:
				profile_obj.user.first_name=first_name
				profile_obj.user.last_name=last_name
				profile_obj.save()

			try:
				login_obj = SocialLogin.objects.get(user=user_obj)
				login_obj.google_access_token = access_token
				login_obj.google_refresh_token = refresh_token
				login_obj.google_client_id = client_id
				login_obj.save()
			except ObjectDoesNotExist:
				social_login_obj = SocialLogin.objects.create(
										user=user_obj,google_client_id=client_id,
										google_id_token=id_token, access_token_expiry=access_token_expiry)

			return Response(status=status.HTTP_200_OK)

		except ObjectDoesNotExist:
			username = first_name+last_name
			chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
			password = get_random_string(6, chars)

			user = User.objects.create(first_name=first_name, last_name=last_name, 
									email=email, username=username, password=password)
			profile = Profile.objects.create(user=user,)
			socail = SocialLogin.objects.create(user=user,google_client_id=client_id,
										google_id_token=id_token, access_token_expiry=access_token_expiry)

			socail.google_access_token = access_token
			socail.google_refresh_token = refresh_token
			socail.google_client_id = client_id
			socail.save()

			return Response(status=status.HTTP_200_OK)

class Facebooklogin(APIView):

	def post(self,request,format="json"):
		provider = 'facebook'
		access_token = request.data.get('access_token', None)

		URL = request.data.get('url', None)
		import urllib.request, json
		with urllib.request.urlopen(URL) as url:
			data = url.read().decode()

		data = json.loads(data)
		email = data['email']
		first_name = data['first_name']
		last_name = data['last_name']
		username = data['name']
		client_id = data['id']
		# access_token = data['access_token']
		try:
			user_obj = User.objects.get(email=email)
			profile_obj = Profile.objects.get(user=user_obj)
			if profile_obj:
				profile_obj.user.first_name=first_name
				profile_obj.user.last_name=last_name
				profile_obj.save()

			try:
				login_obj = SocialLogin.objects.get(user=user_obj)
				login_obj.facebook_access_token = access_token
				login_obj.facebook_client_id = client_id
				login_obj.save()
			except ObjectDoesNotExist:
				social_login_obj = SocialLogin.objects.create(user=user_obj,facebook_client_id=client_id)
			return Response(status=status.HTTP_200_OK)

		except ObjectDoesNotExist:
			if username:
				username = first_name+last_name
			chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
			password = get_random_string(6, chars)

			user = User.objects.create(first_name=first_name, last_name=last_name, 
									email=email, username=username, password=password)
			profile = Profile.objects.create(user=user,)
			socail = SocialLogin.objects.create(user=user,facebook_client_id=client_id)

			socail.facebook_access_token = access_token
			socail.facebook_client_id = client_id
			socail.save()
			return Response(status=status.HTTP_200_OK)
"""
This class is for displaying the user's profile data
"""
class UserProfile(APIView):
	"""
	This function takes data from 3 diffrent models(profile, game, dc)
	and returns required fields on API(user's profile).
	"""
	def get(self,request,format="json"):
		profile  = Profile.objects.filter(user = request.user)
		proserializer = UserSerializer(profile,many=True)
		prodata = proserializer.data
		for pdata in prodata:
			user_obj = User.objects.get(id = pdata['user'])
			pdata['username'] = user_obj.username

		game = GameCollection.objects.filter(user = request.user)
		gameserializer = GameCollectionSerializer(game,many=True)
		gamedata = gameserializer.data
		for gdata in gamedata:
			gdata = gdata

		dc_follower  = FollowUser.objects.filter(follower=request.user).count()
		dc_following = FollowUser.objects.filter(following=request.user).count()
	
		all_data = {}
		all_data['username']=pdata['username']
		all_data['id']=pdata['id']
		all_data['state']=pdata['state']
		all_data['country']=pdata['country']
		all_data['game']=gdata['game']
		all_data['follower']=dc_follower
		all_data['following']=dc_following

		return Response(all_data,status = status.HTTP_200_OK)