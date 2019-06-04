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
	def get(self,request,format="json"):
		follower_user = User.objects.get(id=request.GET.get('follower', None))
		qs = FollowUser.objects.filter(follower=follower_user)

		response = [userfollow for userfollow in qs.values()]

		return JsonResponse(response, safe=False)

	def post(self, request, format="json"):
		follower_user = User.objects.get(id=self.request.user.id)
		following_user = User.objects.get(id=request.data.get('following', None))
		
		response = FollowUser.objects.create(
							following=following_user,
							follower=follower_user)

		return Response(status=status.HTTP_200_OK)


	def put(self, request, format="json"):
		follower_user = User.objects.get(id=self.request.user.id)
		following_user = User.objects.get(id=request.data.get('following', None))
		follow = request.data.get('follow', None)
		unfollow = request.data.get('unfollow', None)
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
				count_followr = 0
				qs = FollowUser.objects.filter(follower=follower_user)
				for userfollows in qs.values():
					count = userfollows.get("follow_count")
					if count == 0 or count == None:
						count = 1

				count_followr = count_followr + count
				user_follow_obj.save()

			if unfollow  == 'True':
				user_follow_obj.created_at=None
				user_follow_obj.delete()
			else:
				user_follow_obj.created_at=datetime.datetime.now()
				user_follow_obj.save()

			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

class HotorNotSwipe(APIView):
	def get(self,request,format="json"):
		user = User.objects.get(id=self.request.user.id)
		likegames = LikeGame.objects.filter(user=user)

		response = []
		game_ids = []
		game_category = {}
		category_ids = []

		if not likegames:
			game_qs = Game.objects.filter(hotornot=True,game_status="published")
			games = [game for game in game_qs.values()]
			response = games
		else:
			for likegame in likegames:
				game_ids.append(likegame.game.id)
				# game_category.append(likegame.game.category)
				# print(likegame.game.category)
				# game = Game.objects.get(id=likegame.game_id, hotornot=True)
				# response.append(model_to_dict(game))
			games = Game.objects.filter(game_status="published", id__in=game_ids)
			for game_obj in games:
				game_obj_dict = model_to_dict(game_obj)
				# game_category.append(game_obj.category)
				for cat in list(game_obj_dict['category']):
					game_category[cat.id]=cat.category_name
					category_ids.append(cat.id)
				# game_obj_dict['category']= game_category
				# response.append(game_obj_dict)
			category_qs = GameCategory.objects.filter(id__in=set(category_ids))
			game_objs = Game.objects.filter(category__in=list(category_qs), hotornot=True)
			for game_object in game_objs:
				if game_object.id not in game_ids:
					game_ids.append(game_object.id)
					game_object_dict = model_to_dict(game_object)
					for cat in list(game_obj_dict['category']):
						game_category[cat.id]=cat.category_name
					game_object_dict['category']= game_category
					response.append(game_object_dict)

			game_collection = GameCollection.objects.filter(user=user, game__hotornot=True)
			for game_coll in game_collection:
				gameobj = Game.objects.get(name=game_coll.game)
				if gameobj.id not in game_ids:
					game_ids.append(gameobj.id)
					gameobj_dict=model_to_dict(gameobj)
					for cat in list(gameobj_dict['category']):
						game_category[cat.id]=cat.category_name
					gameobj_dict['category']= game_category
					response.append(gameobj_dict)

		return JsonResponse(response, safe=False)

class DiscoveryModeHotorNot(APIView):
	def get(self,request,format="json"):
		user = User.objects.get(id=self.request.user.id)
		game_obj = Game.objects.get(id=request.GET.get('game', None))

		game_obj_dict = model_to_dict(game_obj)
		try:
			response = {}
			categories = {}
			for cat in list(game_obj_dict['category']):
				categories[cat.id]=cat.category_name
			game_obj_dict['category'] = categories
			game_extend_obj = GameExtend.objects.get(game__name=game_obj.name)
			game_extend_obj_dict = model_to_dict(game_extend_obj)
			# category = GameCategory.objects.get(category_name=game_obj.category)

			response.update(game_obj_dict)
			response.update(game_extend_obj_dict)
			# response['category'] = category.category_name
			try:
				game_rating_obj = RateGame.objects.get(user=user, game__name=game_obj.name)
				game_rating_dict = model_to_dict(game_rating_obj)

				response.update(game_rating_dict)
			except ObjectDoesNotExist:
				return JsonResponse(response)

			return JsonResponse(response)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)


class DiscoveryModeSwipe(APIView):
	def get(self,request,format="json"):
		user = User.objects.get(id=self.request.user.id)

		qs = LikeGame.objects.filter(user=user)

		response = []
		game_ids = []
		game_category = {}
		category_ids = []
		if not qs:
			game_qs = Game.objects.filter(game_status="published")
			response = [game for game in game_qs.values()]
		else:
			for obj in qs:
				game_ids.append(obj.game.id)
				# game_category.append(obj.game.category)
				# game_category.append(obj.game.category.id)

			games = Game.objects.filter(game_status="published", id__in=game_ids)
			for game_obj in games:
				game_obj_dict = model_to_dict(game_obj)
				# game_category.append(game_obj.category)
				for cat in list(game_obj_dict['category']):
					game_category[cat.id]=cat.category_name
					category_ids.append(cat.id)
				game_obj_dict['category']= game_category
				response.append(game_obj_dict)
			category_qs = GameCategory.objects.filter(id__in=set(category_ids))
			game_objs = Game.objects.filter(game_status="published",category__in=list(category_qs)).exclude(id__in=game_ids)
			for game in game_objs:				
				game_ids.append(game.id)
				game_dict = model_to_dict(game)
				for cat in list(game_dict['category']):
					game_category[cat.id]=cat.category_name
				game_dict['category']= game_category
				response.append(game_dict)
			game_collection = GameCollection.objects.filter(user=user)
			if not game_collection:
				gameobj = Game.objects.filter(game_status="published").exclude(id__in=game_ids)
				response.append([game for game in gameobj.values()])
			else:
				for game_coll in game_collection:
					gameobj = Game.objects.get(name=game_coll,game_status="published")
					if gameobj.id not in game_ids:
						gameobj_dict=model_to_dict(gameobj)
						for cat in list(gameobj_dict['category']):
							game_category[cat.id]=cat.category_name
						gameobj_dict['category']= game_category
						response.append(gameobj_dict)
		return JsonResponse(response, safe=False)
