import datetime
import json
from django.core import serializers
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import *
from registration.models import Profile
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

class GameCorrection(APIView):

	def post(self, request, format="json"):
		response = Game.objects.create(**request.data)
		return Response(status=status.HTTP_201_CREATED)

class UserFollow(APIView):
	def get(self,request,format="json"):
		follower_user = User.objects.get(id=request.GET.get('follower', None))
		qs = FollowUser.objects.filter(follower=follower_user)

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

class GameRating(APIView):
	def post(self, request, format="json"):
		user = User.objects.get(id=request.data.get('user', None))
		game = Game.objects.get(id=request.data.get('game', None))
		game_rating = request.data.get('game_rating', None)

		game_rating_obj = RateGame.objects.create(user=user, 
							game=game,game_rating=game_rating)

		return Response(status=status.HTTP_200_OK)

	def put(self, request, format="json"):
		user = User.objects.get(id=request.data.get('user', None))
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
			return Response(status=status.HTTP_400_BAD_REQUEST)

class GameFollow(APIView):
	def post(self, request, format="json"):
		user = User.objects.get(id=request.data.get('user', None))
		game = Game.objects.get(id=request.data.get('game', None))
		follow = request.data.get('follow', None)

		game_follow_obj = FollowGame.objects.create(user=user,game=game)

		return Response(status=status.HTTP_200_OK)

	def put(self, request, format="json"):
		user = User.objects.get(id=request.data.get('user', None))
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
		user = User.objects.get(id=request.GET.get('user', None))
		game_coll_qs = GameCollection.objects.filter(user=user)
		games_names = []
		for game_coll in game_coll_qs:
			games_names.append(game_coll.game)

		response = {}
		game_qs = Game.objects.filter(name__in=games_names)
		for game_obj in game_qs:
			response[game_obj.name] = {}
			# game_extend_obj = GameExtend.objects.get(game__name=game_obj.name)
			# game_obj.__dict__.update(game_extend_obj.__dict__)
			# response.append(game_obj.__dict__)
			response[game_obj.name].update(like_count = game_obj.like_count)
			response[game_obj.name].update(dislike_count = None)
		return JsonResponse(response)

	def post(self, request, format="json"):
		user = User.objects.get(id=request.data.get('user', None))
		game = Game.objects.get(id=request.data.get('game', None))
		game_collected = request.data.get('game_collected', None)

		game_collection_obj = GameCollection.objects.create(user=user,game=game)

		return Response(status=status.HTTP_200_OK)

	def put(self, request, format="json"):
		user = User.objects.get(id=request.data.get('user', None))
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
			return Response(status=status.HTTP_400_BAD_REQUEST)

class Ugc(APIView):
	def get(self, request, format="json"):
		game_obj = Game.objects.get(id=request.GET.get('game', None))
		try:
			response = {}
			ugc_obj = UGC.objects.get(game__name=game_obj.name)
			ugc_comment = UGCComment.objects.filter(ugc__ugc_title=ugc_obj.ugc_title)
			response[ugc_obj.ugc_title] = {}
			response[ugc_obj.ugc_title].update(user=ugc_obj.user.username)
			response[ugc_obj.ugc_title].update(comments_count=ugc_comment.count())

			return JsonResponse(response)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

	def post(self, request, format="json"):
		user = User.objects.get(id=request.data.get('user', None))
		ugc_title = request.data.get('ugc_title', None)
		like_count = request.data.get('like_count', None)

		ugc_obj = UGC.objects.create(user=user,
								ugc_title=ugc_title,
								like_count=like_count)

		return Response(status=status.HTTP_200_OK)

	def put(self, request, format="json"):
		user = User.objects.get(id=request.data.get('user', None))
		ugc_title = request.data.get('ugc_title', None)
		like_count = request.data.get('like_count', None)

		try:
			ugc_obj = UGC.objects.get(user=user,
								ugc_title=ugc_title)
			if ugc_obj.like_count != like_count:
				ugc_obj.like_count = like_count
				ugc_obj.created_at=datetime.datetime.now()
				ugc_obj.save()

			else:
				ugc_obj.created_at=datetime.datetime.now()
				ugc_obj.save()
			
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

class Ugclikes(APIView):
	def post(self, request, format="json"):
		user = User.objects.get(id=request.data.get('user', None))
		ugc = UGC.objects.get(id=request.data.get('ugc', None))
		like_type = request.data.get('like_type', None)
		
		ugc_like_obj = UGCLike.objects.create(user=user,
								ugc=ugc,
								like_type=like_type)

		return Response(status=status.HTTP_200_OK)

	def put(self, request, format="json"):
		user = User.objects.get(id=request.data.get('user', None))
		ugc = UGC.objects.get(id=request.data.get('ugc', None))
		like_type = request.data.get('like_type', None)

		try:
			ugc_like_obj = UGCLike.objects.get(
									user=user,ugc=ugc)
			if ugc_like_obj.like_type != like_type:
				ugc_like_obj.like_type = like_type
				ugc_like_obj.created_at=datetime.datetime.now()
				ugc_like_obj.save()

			else:
				ugc_like_obj.created_at=datetime.datetime.now()
				ugc_like_obj.save()

			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

class UgcComment(APIView):
	def get(self, request, format="json"):
		response = {}
		ugc_comments = UGCComment.objects.all().order_by('-created_at')

		for comment in ugc_comments:
			comment_dict = model_to_dict(comment)
			response[comment.game.name] = {}
			response[comment.game.name].update(user__username=comment.user.username)
			response[comment.game.name].update(ugc__ugc_title=comment.ugc.ugc_title)
			response[comment.game.name].update(ugc_comment=comment.ugc_comment)
			response[comment.game.name].update(id=comment.id)

		return JsonResponse(response)

	def post(self, request, format="json"):
		user = User.objects.get(id=request.data.get('user', None))
		ugc = UGC.objects.get(id=request.data.get('ugc', None))
		game = Game.objects.get(id=request.data.get('game', None))
		ugc_comment = request.data.get('ugc_comment', None)
		
		ugc_comment_obj = UGCComment.objects.create(user=user,
								ugc=ugc,game=game,
								ugc_comment=ugc_comment)

		return Response(status=status.HTTP_200_OK)

	def put(self, request, format="json"):
		user = User.objects.get(id=request.data.get('user', None))
		ugc = UGC.objects.get(id=request.data.get('ugc', None))
		game = Game.objects.get(id=request.data.get('game', None))
		ugc_comment = request.data.get('ugc_comment', None)
		try:
			ugc_comment_obj = UGCComment.objects.get(user=user,
									ugc=ugc,game=game)
			if ugc_comment_obj.ugc_comment!=ugc_comment:
				ugc_comment_obj.ugc_comment=ugc_comment
				ugc_comment_obj.created_at=datetime.datetime.now()
				ugc_comment_obj.updated_at=datetime.datetime.now()
				ugc_comment_obj.save()

			else:
				ugc_comment_obj.created_at=datetime.datetime.now()
				ugc_comment_obj.updated_at=datetime.datetime.now()
				ugc_comment_obj.save()
		
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

class UgcCommentLike(APIView):
	def post(self, request, format="json"):
		user = User.objects.get(id=request.data.get('user', None))
		ugc_comment = UGCComment.objects.get(id=request.data.get('ugc_comment', None))
		ugc_comment_like = request.data.get('ugc_comment_like', None)

		ugc_comment_like_obj = UGCCommentLike.objects.create(user=user,
								ugc_comment=ugc_comment)

		return Response(status=status.HTTP_200_OK)

	def put(self, request, format="json"):
		user = User.objects.get(id=request.data.get('user', None))
		ugc_comment = UGCComment.objects.get(id=request.data.get('ugc_comment', None))
		ugc_comment_like = request.data.get('ugc_comment_like', None)

		try:
			ugc_comment_like_obj = UGCCommentLike.objects.get(
										user=user,
										ugc_comment=ugc_comment)
			if ugc_comment_like == 'False':
				ugc_comment_like_obj.created_at=None
				ugc_comment_like_obj.save()

			else:
				ugc_comment_like_obj.created_at=datetime.datetime.now()
				ugc_comment_like_obj.save()

			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

class CreateGame(APIView):
	def get(self, request, format="json"):
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

	def post(self, request, format="json"):
		# game_obj = Game.objects.create(name=name,year_published=year_published,
		# 			minimum_players=minimum_players,maximum_players=maximum_players,
		# 			mfg_suggested_ages=mfg_suggested_ages,
		# 			minimum_playing_time=minimum_playing_time,
		# 			maximum_playing_time=maximum_playing_time,designer=designer,
		# 			artist=artist,publisher=publisher,category=category,
		# 			mechanism=mechanism,views=views,like_count=like_count,
		# 			status=status,hotornot=hotornot,upc=upc,origin=origin)

		# fields = [f for f in request.data]
		# for f in fields:
		# 	# setattr(request,f, request.get(f,
		# 	getattr(request,f)
		# 	# ))
		# print (request, '=============================')
		# request.save()


		game_obj = Game.objects.create(**request.data)
		# game_data = Game.objects.get(game=game_obj.name)
		# game_extend_obj = GameExtend.objects.create(game=game_data,**request.data)
		return Response(status=status.HTTP_200_OK)

	def put(self, request, format="json"):
		name = request.data.get('name', None)
		try:
			game_obj = Game.objects.get(name=name)
			game_obj.__dict__.update(**request.data)
			game_obj.updated_at = datetime.datetime.now()
			game_obj.save()
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

class GameExtension(APIView):
	def post(self, request, format="json"):
		game_data = Game.objects.get(id=request.data.pop('game'))
		game_extend_obj = GameExtend.objects.create(game=game_data,**request.data)
		return Response(status=status.HTTP_200_OK)

	def put(self, request, format="json"):
		game_data = Game.objects.get(id=request.data.pop('game'))
		try:
			game_extend_obj = GameExtend.objects.get(game=game_data)
			game_extend_obj.__dict__.update(**request.data)
			game_extend_obj.updated_at = datetime.datetime.now()
			game_extend_obj.save()
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

class TrendingGames(APIView):
	def get(self,request,format="json"):
		game_qs = Game.objects.all().order_by('-like_count')

		games = {}
		for game_obj in game_qs:
			games[game_obj.name]={}
			# game_extend_obj = GameExtend.objects.get(game__name=game_obj.name)
			# game_obj.__dict__.update(game_extend_obj.__dict__)
			games[game_obj.name].update(like_count = game_obj.like_count)
			games[game_obj.name].update(dislike_count = None)
		return JsonResponse(games)

class LikeGames(APIView):
	def post(self,request,format="json"):
		user = User.objects.get(id=request.data.get('user', None))
		game = Game.objects.get(id=request.data.get('game', None))
		game_like = request.data.get('game_like', None)

		like_game_obj = LikeGame.objects.create(user=user,
								game=game,game_like=game_like)
		response = like(game_like,game)
		return response

	def put(self,request,format="json"):
		user = User.objects.get(id=request.data.get('user', None))
		game = Game.objects.get(id=request.data.get('game', None))
		game_like = request.data.get('game_like', None)
		try:
			like_game_obj = LikeGame.objects.get(user=user,game=game)
			if game_like == 'dislike':
				like_game_obj.game_like=game_like
				like_game_obj.save()
				response = like(game_like,game)
				return response

			else:
				like_game_obj.created_at=datetime.datetime.now()
				like_game_obj.game_like=game_like
				like_game_obj.save()
				response = like(game_like,game)
				return response
					
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

def like(game_like, game):
	if game_like == 'like':
		try:
			game_obj = Game.objects.get(name=game.name)
			game_obj.like_count += 1
			game_obj.save()
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)
	else:
		try:
			game_obj = Game.objects.get(name=game.name)
			game_obj.like_count -= 1
			game_obj.save()
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

class UGCReportView(APIView):
	def post(self,request,format="json"):
		user = User.objects.get(id=request.data.get('user', None))
		ugc = UGC.objects.get(id=request.data.get('ugc', None))
		ugc_report = UGCReport.objects.create(user=user,ugc=ugc)
		return Response(status=status.HTTP_200_OK)

class GameFollowingFeed(APIView):
	def get(self,request,format="json"):
		follower = User.objects.get(id=request.GET.get('follower', None))

		response = {}
		follow_game = []
		following_users = []

		follow_game_qs = FollowGame.objects.filter(user=follower)
		for follow_game_obj in follow_game_qs:
			follow_game.append(follow_game_obj.game.id)
		game_qs = Game.objects.filter(id__in=follow_game).order_by('-like_count')

		for game_obj in game_qs:
			response[game_obj.name]={}
			# game_extend_obj = GameExtend.objects.get(game__name=game_obj['name'])
			# game_obj.update(game_extend_obj.__dict__)
			# response.append(game_obj)
			response[game_obj.name].update(like_count = game_obj.like_count)
			response[game_obj.name].update(dislike_count = None)


		user_follow_qs = FollowUser.objects.filter(
							follower=follower)
		for user_follow_obj in user_follow_qs:
			following_users.append(user_follow_obj.following)
		game_collection_qs = GameCollection.objects.filter(
							user__in=following_users).order_by('-created_at')

		for game_collection in game_collection_qs:
			if game_collection.game.id not in follow_game:
				game_object = Game.objects.get(name=game_collection.game)
				response[game_object.name] = {}
				# game_extend_obj = GameExtend.objects.get(game__name=game_obj.name)
				# game_obj.__dict__.update(game_extend_obj.__dict__)
				# response.append(game_obj.__dict__)
				response[game_object.name].update(like_count = game_object.like_count)
				response[game_object.name].update(dislike_count = None)
		
		return JsonResponse(response)

class UserFollowingFeed(APIView):
	def get(self,request,format="json"):
		follower = User.objects.get(id=request.GET.get('follower', None))
		response = {}
		user_follow_qs = FollowUser.objects.filter(
							follower=follower)
		following_users = []
		for user_follow_obj in user_follow_qs:
			following_users.append(user_follow_obj.following)

		ugc_qs = UGC.objects.filter(user__in=following_users).\
							order_by('-created_at')
		for ugc_obj in ugc_qs:
			response[ugc_obj.user.username]={}
			response[ugc_obj.user.username].update(ugc_title = ugc_obj.ugc_title)
			
		return JsonResponse(response)

class HotorNotSwipe(APIView):
	def get(self,request,format="json"):
		user = User.objects.get(id=request.GET.get('user', None))
		qs = Game.objects.filter(hotornot='True')
		response = {}
		game_ids = []
		for game_obj in qs:
			response[game_obj.name]={}
			game_ids.append(game_obj.id)
			# game_extend_obj = GameExtend.objects.get(game__name=game_obj.name)
			# game_obj.__dict__.update(game_extend_obj.__dict__)
			# response.append(game_obj.__dict__)
			response[game_obj.name].update(like_count = game_obj.like_count)
			response[game_obj.name].update(dislike_count = None)

		likegames = LikeGame.objects.filter(user=user)
		for likegame in likegames:
			if likegame.game_id not in game_ids:
				game = Game.objects.get(id=likegame.game_id)
				response[game.name]={}
				# game_extend_obj = GameExtend.objects.get(game__name=game_obj.name)
				# game_obj.__dict__.update(game_extend_obj.__dict__)
				# response.append(game_obj.__dict__)
				response[game.name].update(like_count = game.like_count)
				response[game.name].update(dislike_count = None)

		return JsonResponse(response)

class DiscoveryModeHotorNot(APIView):
	def get(self,request,format="json"):
		response = {}
		game_obj = Game.objects.get(id=request.GET.get('game', None))
		response[game_obj.name] = {}
		# game_extend_obj = GameExtend.objects.get(game__name=game_obj.name)
		# game_obj.__dict__.update(game_extend_obj.__dict__)
		# response.append(game_obj.__dict__)
		response[game_obj.name].update(like_count = game_obj.like_count)
		response[game_obj.name].update(dislike_count = None)

		return JsonResponse(response)

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
			response[game_obj.name]={}
			game_category.append(game_obj.category)
			# game_extend_obj = GameExtend.objects.get(game__name=game_obj.name)
			# game_obj.__dict__.update(game_extend_obj.__dict__)
			# response.append(game_obj.__dict__)
			response[game_obj.name].update(like_count = game_obj.like_count)
			response[game_obj.name].update(dislike_count = None)


		game_objs = Game.objects.filter(category__in=game_category)
		for game in game_objs:
			if game.id not in game_ids:
				response[game.name] = {}
				# game_extend = GameExtend.objects.get(game__name=game.name)
				# game.__dict__.update(game_extend_obj.__dict__)
				# response.append(game.__dict__)
				response[game.name].update(like_count = game.like_count)
				response[game.name].update(dislike_count = None)


		game_collection = GameCollection.objects.filter(user=user)
		for game_coll in game_collection:
			gameobj = Game.objects.get(name=game_coll.game)
			if game.id not in game_ids:
				response[gameobj.name] = {}
				# game_extend = GameExtend.objects.get(game__name=game.name)
				# game.__dict__.update(game_extend_obj.__dict__)
				# response.append(game.__dict__)
				response[gameobj.name].update(like_count = gameobj.like_count)
				response[gameobj.name].update(dislike_count = None)

		return JsonResponse(response)

class UserCommonGame(APIView):
	def get(self,request,format="json"):
		follower = User.objects.get(id=request.GET.get('user', None))
		following = User.objects.get(id=request.GET.get('other_user', None))
		follower_games = FollowGame.objects.filter(user=follower)
		following_games = FollowGame.objects.filter(user=following)
	
		followergames = {}
		followinggames = {}
		for follower_game in follower_games:
			game = Game.objects.get(name=follower_game.game)
			followergames[game.name] = {}
			# game_extend = GameExtend.objects.get(game__name=game.name)
			# game.__dict__.update(game_extend.__dict__)
			# followergames.append(game.__dict__)
			followergames[game.name].update(like_count = game.like_count)
			followergames[game.name].update(dislike_count = None)


		for following_game in following_games:
			game_obj = Game.objects.get(name=following_game.game)
			followinggames[game_obj.name] = {}
			# game_extend_obj = GameExtend.objects.get(game__name=game.name)
			# game_obj.__dict__.update(game_extend_obj.__dict__)
			# followinggames.append(game_obj.__dict__)
			followinggames[game_obj.name].update(like_count = game_obj.like_count)
			followinggames[game_obj.name].update(dislike_count = None)

		response = followergames and followinggames
		return JsonResponse(response)

class Search(APIView):
	def get(self, request, format="json"):
		data = request.GET.get('data', None)
		game_name_qs = Game.objects.filter(name=data).order_by('name')
		print (game_name_qs, '-----------------------')
		game_category_qs = Game.objects.filter(category__category_name=data).order_by('name')
		print (game_category_qs, '//////////////////////////')
		game_tag_qs = GameTag.objects.filter(tag_name__tag=data).order_by('tag_name')
		print (game_tag_qs, '=============================')


		qs = game_name_qs.union(game_category_qs)

		game_ids = []
		for obj in game_name_qs:
			game_ids.append(obj.id)

		objs = {}

		for obj in game_name_qs:
			objs.update(obj)


		return Response(status=status.HTTP_200_OK)
