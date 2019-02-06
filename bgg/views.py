import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import *
from registration.models import Profile
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist


class GameCorrection(APIView):

	def post(self, request, format="json"):
		response = Game.objects.create(**request.data)
		return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
def user_auth_status(request, format="json"):
	username = request.data.get('username', None)
	profile_obj = Profile.objects.get(user__username=username)
	data =[]
	user = profile_obj.user
	if user.is_authenticated():
		return Response(user.is_authenticated,status=status.HTTP_200_OK)
	else:
		return Response(user.is_authenticated,status=status.HTTP_401_UNAUTHORIZED)


class UserFollow(APIView):
	def post(self, request, format="json"):
		follower_user = User.objects.get(username=request.data.get('follower', None))
		following_user = User.objects.get(username=request.data.get('following', None))
		
		response = FollowUser.objects.create(
							following=following_user,
							follower=follower_user)

		print (response)
		return Response(status=status.HTTP_200_OK)

	def put(self, request, format="json"):
		follower_user = User.objects.get(username=request.data.get('follower', None))
		following_user = User.objects.get(username=request.data.get('following', None))
		user_follow = request.data.get('user_follow', None)
		try:
			user_follow_obj = FollowUser.objects.get(
							following=following_user,
							follower=follower_user
							)
			if user_follow == 'False':
				user_follow_obj.created_at=None
				user_follow_obj.save()

			else:
				user_follow_obj.created_at=datetime.datetime.now()
				user_follow_obj.save()
			
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:

			response = FollowUser.objects.create(
							following=following_user,
							follower=follower_user)
			return Response(status=status.HTTP_200_OK)


class GameRating(APIView):
	def post(self, request, format="json"):
		user = User.objects.get(username=request.data.get('user', None))
		game = Game.objects.get(name=request.data.get('game', None))
		game_rating = request.data.get('game_rating', None)

		game_rating_obj = RateGame.objects.create(user=user, 
							game=game,game_rating=game_rating)

		return Response(status=status.HTTP_200_OK)

	def put(self, request, format="json"):
		user = User.objects.get(username=request.data.get('user', None))
		game = Game.objects.get(name=request.data.get('game', None))
		game_rating = request.data.get('game_rating', None)

		try:
			game_rating_obj = RateGame.objects.get(user=user, 
							game=game)
			if game_rating_obj.game_rating != game_rating:
				game_rating_obj.game_rating = game_rating
				game_rating_obj.created_at=datetime.datetime.now()
				game_rating_obj.save()

			else:
				game_rating_obj.created_at=datetime.datetime.now()
				game_rating_obj.save()

			return Response(status=status.HTTP_200_OK)
		
		except ObjectDoesNotExist:
			game_rating_obj = RateGame.objects.create(user=user, 
							game=game,game_rating=game_rating)

			return Response(status=status.HTTP_200_OK)
