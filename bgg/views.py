import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import *
from registration.models import Profile
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse


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
	def post(self, request, format="json"):
		user = User.objects.get(id=request.data.get('user', None))
		ugc = UGC.objects.get(id=request.data.get('ugc', None))
		game = Game.objects.get(id=request.data.get('game', None))
		ugc_comments = request.data.get('ugc_comments', None)
		
		ugc_comment_obj = UGCComment.objects.create(user=user,
								ugc=ugc,game=game,
								ugc_comments=ugc_comments)

		return Response(status=status.HTTP_200_OK)

	def put(self, request, format="json"):
		user = User.objects.get(id=request.data.get('user', None))
		ugc = UGC.objects.get(id=request.data.get('ugc', None))
		game = Game.objects.get(id=request.data.get('game', None))
		ugc_comments = request.data.get('ugc_comments', None)
		try:
			ugc_comment_obj = UGCComment.objects.get(user=user,
									ugc=ugc,game=game)
			if ugc_comment_obj.ugc_comments!=ugc_comments:
				ugc_comment_obj.ugc_comments=ugc_comments
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
	def post(self, request, format="json"):
		game_obj = Game.objects.create(**request.data)
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
		game = Game.objects.get(id=request.data.get('game', None))
		game_like = request.data.get('game_like')
		game_qs = Game.objects.all().order_by('-like_count')
		response = []
		for game_obj in game_qs:
			response.append(game_obj)
		print (response ,'=================================')
		return Response(response)

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
				like_game_obj.created_at=None
				like_game_obj.save()
				response = like(game_like,game)
				return response

			else:
				like_game_obj.created_at=datetime.datetime.now()
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