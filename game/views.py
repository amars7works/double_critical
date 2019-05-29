import datetime
import json
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core import serializers
from game.models import *
from ugc.models import *
from dc.models import *
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

class GameCorrection(APIView):

	def post(self, request, format="json"):
		response = Game.objects.create(**request.data)
		return Response(status=status.HTTP_201_CREATED)

class GameRating(APIView):
	def get(self, request, format="json"):
		user = User.objects.get(id=self.request.user.id)
		game = Game.objects.get(id=request.GET.get('game', None))
		try:
			game_rating_obj = RateGame.objects.get(user=user, game=game)
			game_rating_dict = model_to_dict(game_rating_obj)
			return JsonResponse(game_rating_dict)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

	def post(self, request, format="json"):
		user = User.objects.get(id=self.request.user.id)
		game = Game.objects.get(id=request.data.get('game', None))
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

class GameFollow(APIView):
	def get(self, request, format="json"):
		game = Game.objects.get(id=request.GET.get('game', None))
		game_follow_qs = FollowGame.objects.filter(game=game)
		response = []
		for game_follow_obj in game_follow_qs.values():
			if game_follow_obj['created_at']:
				response.append(game_follow_obj)

		return JsonResponse(response, safe=False)


	def post(self, request, format="json"):
		user = User.objects.get(id=self.request.user.id)
		game = Game.objects.get(id=request.data.get('game', None))
		follow = request.data.get('follow', None)

		if follow == 'True':
			game_follow_obj = FollowGame.objects.create(user=user,game=game)
			return Response(status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, format="json"):
		user = User.objects.get(id=self.request.user.id)
		game = Game.objects.get(id=request.data.get('game', None))
		follow = request.data.get('follow', None)

		try:
			game_follow_obj = FollowGame.objects.get(user=user,game=game)
			if follow == 'False':
				game_follow_obj.created_at=None
				game_follow_obj.save()
			else:
				game_follow_obj.created_at=datetime.datetime.now()
				game_follow_obj.save()
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

class CollectingGame(APIView):
	def get(self, request, format="json"):
		user = User.objects.get(id=self.request.user.id)
		game_coll_qs = GameCollection.objects.filter(user=user)
		games_names = []
		for game_coll in game_coll_qs:
			games_names.append(game_coll.game)

		game_qs = Game.objects.filter(name__in=games_names)
		response = [game_obj for game_obj in game_qs.values()]
		return JsonResponse(response, safe=False)

	def post(self, request, format="json"):
		user = User.objects.get(id=self.request.user.id)
		game = Game.objects.get(id=request.data.get('game', None))
		game_collected = request.data.get('game_collected', None)
		try:
			game_collection_obj = GameCollection.objects.get(user=user,game=game)
			if game_collected == 'False':
				game_collection_obj.created_at=None
				game_collection_obj.save()
			else:
				game_collection_obj.created_at=datetime.datetime.now()
				game_collection_obj.save()
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			if game_collected == 'True':
				game_collection_obj = GameCollection.objects.create(user=user,game=game)
				return Response(status=status.HTTP_200_OK)

class CreateGame(APIView):
	def get(self, request, format="json"):
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

			return JsonResponse(response)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

	def post(self, request, format="json"):
		name = request.data.get('name', None)
		year_published = request.data.get('year_published', None)
		minimum_players = request.data.get('minimum_players', None)
		maximum_players = request.data.get('maximum_players', None)
		mfg_suggested_ages = request.data.get('mfg_suggested_ages', None)
		minimum_playing_time = request.data.get('minimum_playing_time', None)
		maximum_playing_time = request.data.get('maximum_playing_time', None)
		designer = request.data.get('designer', None)
		artist = request.data.get('artist', None)
		publisher = request.data.get('publisher', None)
		mechanism = request.data.get('mechanism', None)
		views = request.data.get('views', None)
		like_count = request.data.get('like_count', None)
		game_status = request.data.get('game_status', None) if request.data.get('game_status', None) else "review"
		hotornot = request.data.get('hotornot', None) if request.data.get('hotornot', None) else False
		upc = request.data.get('upc', None) 
		origin = request.data.get('origin', None) if request.data.get('origin', None) else "publisher"

		expansion = request.data.get('expansion', None)
		expands = request.data.get('expands', None)
		integrates_with = request.data.get('integrates_with', None)
		contains = request.data.get('contains', None)
		contained_in = request.data.get('contained_in', None)
		reimplemented_by = request.data.get('reimplemented_by', None)
		reimplements = request.data.get('reimplements', None)
		family = request.data.get('family', None)
		video_game_adaptation = request.data.get('video_game_adaptation', None)
		note_to_admin = request.data.get('note_to_admin', None)
		data = request.data.get('data', None)
		scan_type = request.data.get('scan_type', None)

		category = GameCategory.objects.filter(category_name__in=request.data.get('category', None))

		game_obj = Game(name=name,year_published=year_published,
					minimum_players=minimum_players,maximum_players=maximum_players,
					mfg_suggested_ages=mfg_suggested_ages,
					minimum_playing_time=minimum_playing_time,
					maximum_playing_time=maximum_playing_time,designer=designer,
					artist=artist,publisher=publisher,
					mechanism=mechanism,views=views,like_count=like_count,
					game_status=game_status,
					hotornot=hotornot,
					upc=upc,
					origin=origin,
					data=data,scan_type=scan_type)
		game_obj.save()
		for cat in category:
			game_obj.category.add(cat)

		game_extend_obj = GameExtend.objects.create(game=game_obj,expansion=expansion,
					expands=expands,integrates_with=integrates_with,contains=contains,
					contained_in=contained_in,reimplemented_by=reimplemented_by,
					reimplements=reimplements,family=family,note_to_admin=note_to_admin,
					video_game_adaptation=video_game_adaptation)

		return Response(status=status.HTTP_201_CREATED)

	# def put(self, request, format="json"):
	# 	name = request.data.get('name', None)
	# 	try:
	# 		game_obj = Game.objects.get(name=name)
	# 		game_obj.__dict__.update(**request.data)
	# 		game_obj.updated_at = datetime.datetime.now()
	# 		game_obj.save()
	# 		return Response(status=status.HTTP_200_OK)
	# 	except ObjectDoesNotExist:
	# 		return Response(status=status.HTTP_400_BAD_REQUEST)

# class GameExtension(APIView):
# 	def post(self, request, format="json"):
# 		game_data = Game.objects.get(id=request.data.pop('game'))
# 		game_extend_obj = GameExtend.objects.create(game=game_data,**request.data)
# 		return Response(status=status.HTTP_200_OK)

# 	def put(self, request, format="json"):
# 		game_data = Game.objects.get(id=request.data.pop('game'))
# 		try:
# 			game_extend_obj = GameExtend.objects.get(game=game_data)
# 			game_extend_obj.__dict__.update(**request.data)
# 			game_extend_obj.updated_at = datetime.datetime.now()
# 			game_extend_obj.save()
# 			return Response(status=status.HTTP_200_OK)
# 		except ObjectDoesNotExist:
# 			return Response(status=status.HTTP_400_BAD_REQUEST)

class TrendingGames(APIView):
	def get(self,request,format="json"):
		game_qs = Game.objects.filter(game_status="published").extra(
					select={"count": 'like_count - dislike_count'}).order_by("-count", "name")

		games = [game for game in game_qs.values()]

		# games = []
		# for game_obj in game_qs:
		# 	game_extend_obj = GameExtend.objects.get(game__name=game_obj.name)
		# 	game_obj_dict = model_to_dict(game_obj)
		# 	game_obj_dict.update(model_to_dict(game_extend_obj))

		return JsonResponse(games, safe=False)

class LikeGames(APIView):
	def get(self,request,format="json"):
		user = User.objects.get(id=self.request.user.id)
		like_game_qs = LikeGame.objects.filter(user=user,
								game_like='like')
		games = []
		for obj in like_game_qs:
			games.append(obj.game.id)

		game_qs = Game.objects.filter(id__in=games)
		response = [game_obj for game_obj in game_qs.values()]

		return JsonResponse(response, safe=False)


	def post(self,request,format="json"):
		user = User.objects.get(id=self.request.user.id)
		game = Game.objects.get(id=request.data.get('game', None))
		game_like = request.data.get('game_like', None)
		try:
			like_game_obj = LikeGame.objects.get(user=user,game=game)
			if game_like == 'dislike':
				game.like_count -= 1
				like_game_obj.game_like=game_like
				like_game_obj.save()
				game.save()
				response = like(game_like,game)
				return response
			else:
				game.dislike_count -= 1
				like_game_obj.created_at=datetime.datetime.now()
				like_game_obj.game_like=game_like
				like_game_obj.save()
				game.save()
				response = like(game_like,game)
				return response
		except ObjectDoesNotExist:
			# return Response(status=status.HTTP_400_BAD_REQUEST)
			like_game_obj = LikeGame.objects.create(user=user,
								game=game,game_like=game_like)
			like_game_obj.views += 1
			like_game_obj.save
			response = like(game_like,game)
			return response

def like(game_like, game_obj):
	if game_like == 'like':
		try:
			# game_obj = Game.objects.get(name=game.name)
			game_obj.like_count += 1
			game_obj.save()
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)
	else:
		try:
			# game_obj = Game.objects.get(name=game_obj.name)
			# game_obj.like_count -= 1
			game_obj.dislike_count += 1
			game_obj.save()
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

class GameFollowingFeed(APIView):
	def get(self,request,format="json"):
		follower = User.objects.get(id=self.request.user.id)

		response = []
		follow_game = []

		follow_game_qs = FollowGame.objects.filter(user=follower)
		for follow_game_obj in follow_game_qs:
			follow_game.append(follow_game_obj.game.id)
		# game_qs = Game.objects.filter(id__in=follow_game).order_by('-like_count')

		ugc_obj = UGC.objects.filter(user=follower, game__in=follow_game).latest('created_at')
		date_from = datetime.datetime.now() - datetime.timedelta(days=1)
		if ugc_obj.created_at.date() == date_from.date() or datetime.date.today():
			response.append(model_to_dict(ugc_obj))

		user_follow_qs = FollowUser.objects.filter(follower__id=follower.id)
		following_users = []
		for user_follow_obj in user_follow_qs:
			following_users.append(user_follow_obj.following)
		if following_users:
			ugc = UGC.objects.filter(user__in=following_users).latest('created_at')
			if ugc_obj != ugc:
				if ugc.created_at.date() == date_from.date() or datetime.date.today():
					response.append(model_to_dict(ugc))

			game_collection = GameCollection.objects.filter(
								user__in=following_users).latest('created_at')

			if game_collection.created_at.date() == date_from.date() or datetime.date.today():
				# if game_collection.game.id not in follow_game:
				game_object = Game.objects.get(name=game_collection.game)
				response.append(model_to_dict(game_object))

		return JsonResponse(response, safe=False)

class UserCommonGame(APIView):
	def get(self,request,format="json"):
		follower = User.objects.get(id=self.request.user.id)
		following = User.objects.get(id=request.GET.get('other_user', None))
		follow_games = FollowGame.objects.filter(
					Q(user=follower) | Q(user=following)
				)
		followgames = list(set(follow_game.game.name for follow_game in follow_games))

		games = Game.objects.filter(name__in=followgames)
		response = [game for game in games.values()]

		return JsonResponse(response, safe=False)

class BarCode(APIView):
	def get(self,request,format="json"):
		scan_data = self.request.query_params.get('Scanner_data', None)
	
		if scan_data:
			games = Game.objects.filter(data=scan_data).values()
			if games:
				game_collections = GameCollection.objects.filter(user=request.user, 
											game__id=games[0]['id']).values()
				if game_collections:
					games[0]['collection'] = True
				else:
					games[0]['collection'] = False
				return JsonResponse(games[0], safe=False)
			else:
				return JsonResponse({"error": "game_not_found"}, status=status.HTTP_404_NOT_FOUND)
		else:
			return JsonResponse({"error":"missing_arguments"},status=status.HTTP_400_BAD_REQUEST )
	
