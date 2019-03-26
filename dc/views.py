import datetime
import json
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import *
from game.models import *
from ugc.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

class UserFollow(APIView):
	# def get(self,request,format="json"):
	# 	follower_user = User.objects.get(id=request.GET.get('follower', None))
	# 	qs = FollowUser.objects.filter(follower=follower_user)

	def post(self, request, format="json"):
		follower_user = User.objects.get(id=request.data.get('follower', None))
		following_user = User.objects.get(id=request.data.get('following', None))
		
		response = FollowUser.objects.create(
							following=following_user,
							follower=follower_user)

		return Response(status=status.HTTP_200_OK)

	def put(self, request, format="json"):
		follower_user = User.objects.get(id=request.data.get('follower', None))
		following_user = User.objects.get(id=request.data.get('following', None))
		follow = request.data.get('follow', None)
		try:
			user_follow_obj = FollowUser.objects.get(
							following=following_user,
							follower=follower_user
							)
			if follow == 'False':
				user_follow_obj.created_at=None
				user_follow_obj.save()

			else:
				user_follow_obj.created_at=datetime.datetime.now()
				user_follow_obj.save()
			
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

class HotorNotSwipe(APIView):
	def get(self,request,format="json"):
		user = User.objects.get(id=request.GET.get('user', None))
		qs = Game.objects.filter(hotornot='True')
		response = {}
		game_ids = []
		game_category = []

		for game_obj in qs:
			response[game_obj.name]={}
			game_ids.append(game_obj.id)
			game_category.append(game_obj.category)
			response[game_obj.name].update(like_count = game_obj.like_count)
			response[game_obj.name].update(dislike_count = None)

		likegames = LikeGame.objects.filter(user=user)
		for likegame in likegames:
			if likegame.game_id not in game_ids:
				game = Game.objects.get(id=likegame.game_id)
				response[game.name]={}
			response[game.name].update(like_count = game.like_count)
			response[game.name].update(dislike_count = None)

		game_objs = Game.objects.filter(category__in=game_category)
		for game in game_objs:
			if game.id not in game_ids:
				response[game.name] = {}
				response[game.name].update(like_count = game.like_count)
				response[game.name].update(dislike_count = None)


		game_collection = GameCollection.objects.filter(user=user)
		for game_coll in game_collection:
			gameobj = Game.objects.get(name=game_coll.game)
			if game.id not in game_ids:
				response[gameobj.name] = {}
				response[gameobj.name].update(like_count = gameobj.like_count)
				response[gameobj.name].update(dislike_count = None)

		return JsonResponse(response)

class DiscoveryModeHotorNot(APIView):
	def get(self,request,format="json"):
		game_obj = Game.objects.get(id=request.GET.get('game', None))

		game_obj_dict = model_to_dict(game_obj)
		try:
			response = {}
			game_extend_obj = GameExtend.objects.get(game__name=game_obj.name)
			game_extend_obj_dict = model_to_dict(game_extend_obj)

			response.update(game_obj_dict)
			response.update(game_extend_obj_dict)
			return JsonResponse(response)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)


class DiscoveryModeSwipe(APIView):
	def get(self,request,format="json"):
		user = User.objects.get(id=request.GET.get('user', None))
		if user.is_authenticated():
			qs = LikeGame.objects.filter(user=user,game_like='like').values()
		response = {}

		game_ids = []
		game_category = []
		for obj in qs:
			game_ids.append(obj['game_id'])

		games = Game.objects.filter(id__in=game_ids)
		for game_obj in games:
			# response[game_obj.name]={}
			game_category.append(game_obj.category)
			# response[game_obj.name].update(like_count = game_obj.like_count)
			# response[game_obj.name].update(dislike_count = None)
			response.update(game_name=game_obj.name, game_id=game_obj.id)


		game_objs = Game.objects.filter(category__in=game_category)
		for game in game_objs:
			if game.id not in game_ids:
				# response[game.name] = {}
				# response[game.name].update(like_count = game.like_count)
				# response[game.name].update(dislike_count = None)
				response.update(game_name=game_obj.name, game_id=game_obj.id)


		game_collection = GameCollection.objects.filter(user=user)
		for game_coll in game_collection:
			gameobj = Game.objects.get(name=game_coll.game)
			if gameobj.id not in game_ids:
				# response[gameobj.name] = {}
				# response[gameobj.name].update(like_count = gameobj.like_count)
				# response[gameobj.name].update(dislike_count = None)
				response.update(game_name=gameobj.name, game_id=gameobj.id)

		return JsonResponse(response)
