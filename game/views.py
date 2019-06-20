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
from django.conf import settings

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
				game_follow_obj.delete()
			else:
				game_follow_obj.created_at=datetime.datetime.now()
				game_follow_obj.save()
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

class CollectingGame(APIView):
	def get(self, request, format="json"):
		user = User.objects.get(id=self.request.user.id)
		game_collections = GameCollection.objects.filter(user=user)
		game_name_list = []
		for game_collected in game_collections:
			if game_collected.created_at:
				game_name_list.append(game_collected.game)

		games = Game.objects.filter(name__in= game_name_list)
		response = [game for game in games.values()]
		return JsonResponse(response, safe=False)

	def post(self, request, format="json"):
		user = User.objects.get(id=self.request.user.id)
		game_id = Game.objects.get(id=request.data.get('game_id', None))
		game_collected = request.data.get('add_to_collection', None)
		response_data = { "status": "game_not_found" }
		try:
			game_collection_obj = GameCollection.objects.get(game=game_id)
			if not game_collected:
				game_collection_obj.created_at = None
				game_collection_obj.delete()
				response_data['status'] = "removed_from_collection"
			else:
				game_collection_obj.created_at = datetime.datetime.now()
				game_collection_obj.save()
				response_data['status'] = "added_to_collection"
		except ObjectDoesNotExist:
			if game_collected:
				game_collection_obj = GameCollection.objects.create(user=user,game=game_id)
				response_data['status'] = "added_to_collection"
		return Response(status=status.HTTP_200_OK)


class CreateGame(APIView):
	def get(self, request, format="json"):
		game_obj = Game.objects.get(id=request.GET.get('game', None))
		game_obj_dict = model_to_dict(game_obj)
		try:
			response = {}
			categories = {}
			artistss = {}
			publishers = {}
			designers = {}
			mechanisms = {}
			card_images = {}
		
			for cat in list(game_obj_dict['category']):
				categories[cat.id]=cat.category_name
			game_obj_dict['category'] = categories
			for artists in list(game_obj_dict['artist']):
				artistss[artists.id]=artists.artist_name
			game_obj_dict['artist'] = artistss
			for pub in list(game_obj_dict['publisher']):
				publishers['pub.id']=pub.publisher_name
			game_obj_dict['publisher'] = publishers
			for design in list(game_obj_dict['designer']):
				designers[design.id] = design.designer_name
			game_obj_dict['designer'] = designers
			for mecha in list(game_obj_dict['mechanism']):
				mechanisms[mecha.id] = mecha.mechanism
			game_obj_dict['mechanism'] = mechanisms
			game_obj_dict['card_image'] = settings.MEDIA_ROOT+game_obj_dict['card_image'].url
			game_obj_dict['swipe_image'] = settings.MEDIA_ROOT+game_obj_dict['swipe_image'].url
			game_obj_dict['info_image'] = settings.MEDIA_ROOT+game_obj_dict['info_image'].url

			game_extend_obj = GameExtend.objects.get(game__name=game_obj.name)

			game_extend_obj_dict = model_to_dict(game_extend_obj)

			response.update(game_obj_dict)
			response.update(game_extend_obj_dict)

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
		game_status ="review"
		hotornot = False
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
		card_image = request.data.get('card_image', None)
		swipe_image = request.data.get('swipe_image', None)
		info_image = request.data.get('info_image', None)

		game_obj = Game(name=name,year_published=year_published,
					minimum_players=minimum_players,maximum_players=maximum_players,
					mfg_suggested_ages=mfg_suggested_ages,
					minimum_playing_time=minimum_playing_time,
					maximum_playing_time=maximum_playing_time,
					views=views,like_count=like_count,card_image=card_image,
					swipe_image=swipe_image,info_image=info_image,
					game_status=game_status,
					hotornot=hotornot,
					upc=upc,
					origin=origin,
					data=data,scan_type=scan_type)
		game_obj.save()
		cat_list = request.data.get('category', [])
		category = []
		for cat in cat_list:
			try:
				item = GameCategory.objects.get(category_name=cat)
				category.append(item)
			except ObjectDoesNotExist:
				item = GameCategory.objects.create(category_name=cat,status="review")
				category.append(item)
		for cat_item in category:
			game_obj.category.add(cat_item)

		designer_list = request.data.get('designer',[])
		designer = []
		for dig in designer_list:
			try:
				item = Designer.objects.get(designer_name=dig)
				designer.append(item)
			except ObjectDoesNotExist:
				item =Designer.objects.create(designer_name=dig)
				designer.append(item)
			for dig_item in designer:
				game_obj.designer.add(dig_item)
		artist_list = request.data.get('artist', [])
		artist = []
		for art in artist_list:
			try:
				item = Artist.objects.get(artist_name=art)
				artist.append(item)
			except ObjectDoesNotExist:
				item = Artist.objects.create(artist_name=art)
				artist.append(item)
			for atr_item in artist:
				game_obj.artist.add(item)
		pub_list = request.data.get('publisher', [])
		publisher = []
		for pub in pub_list:
			try:
				item = Publisher.objects.get(publisher_name=pub)
				publisher.append(item)
			except ObjectDoesNotExist:
				item = Publisher.objects.create(publisher_name=pub)
				publisher.append(item)
			for pub_item in publisher:
				game_obj.publisher.add(item)
		mecha_list = request.data.get('mechanism',)
		mechanism = []
		for mech in mecha_list:
			try:
				item = Mechanism.objects.get(mechanism = mech)
				mechanism.append(item)
			except ObjectDoesNotExist:
				item = Mechanism.objects.create(mechanism = mech)
				mechanism.append(item)
		for mech_item in mechanism:
			game_obj.mechanism.add(item)

		game_extend_obj = GameExtend.objects.create(game=game_obj,expansion=expansion,
					expands=expands,integrates_with=integrates_with,contains=contains,
					contained_in=contained_in,reimplemented_by=reimplemented_by,
					reimplements=reimplements,family=family,note_to_admin=note_to_admin,
					video_game_adaptation=video_game_adaptation)

		return Response(status=status.HTTP_201_CREATED)


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
				cat = {}
				publishers = {}
				Mechanisms = {}
				artists = {}
				designers ={}
				response = model_to_dict(game_object)
				for categiry in list(response['category']):
					cat[categiry.id]=categiry.category_name
				response['category'] = cat
				for pub in list(response['publisher']):
					publishers[pub.id]=pub.publisher_name
				response['publisher'] = publishers
				for mec in list(response['mechanism']):
					Mechanisms[mec.id]=mec.mechanism
				response['mechanism'] = Mechanisms
				for art in list(response['artist']):
					artists[art.id]=art.artist_name
				response['artist'] = artists
				for dsg in list(response['designer']):
					designers[dsg.id]=dsg.designer_name
				response['designer'] = designers

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
	
class incement_like_count(APIView):
	def put(self,request,format="json"):
		user = User.objects.get(id=self.request.user.id)
		obj_id = LikeLog.objects.get(id=request.GET.get('object_id', None))
		likes_count = request.data.get('likes_count', None)
		if obj_id:
			try:
				social_base = SocialBase.objects.filter(user=user)
				for social in social_base:
					if social.likes_count == likes_count:
						social.likes_count = likes_count
						social.likes_count +=1
					# social.created_at=datetime.datetime.now()
						social.save()
					else:
						social.likes_count -=1
						social.save()
				return Response(status=status.HTTP_200_OK)
			except ObjectDoesNotExist:
				return Response(status=status.HTTP_400_BAD_REQUEST)


class GameFeeds(APIView):
	"""
	parameter: game
	getting the data, details like username, title, game name,
	game description, game id and comment coiunt
	return: game_dict 
	"""
	def get(self,request,format="json"):
		following = User.objects.get(id=request.GET.get('following',None))
		response = []
		if following:
			game_feed = Gamefeeds.objects.filter(user=following).order_by('-created_at')
			for game_feed_obj in game_feed:
				game_dict = {}
				game_comments = Gamefeeds.objects.filter(game_title=game_feed_obj.game_title).count()

				game_dict['game_title']=game_feed_obj.game_title
				game_dict['user']=game_feed_obj.user.username
				game_dict['comments_count']=game_comments
				game_dict['game_id']=game_feed_obj.id
				game_dict['game_description']=game_feed_obj.game_description
				game_dict['like_count']=game_feed_obj.like_count
				response.append(game_dict)
			# return JsonResponse(game_dict,safe=False)
		return Response(response, status = status.HTTP_200_OK)


	"""
	parameters: game, game_title, game_description
	this methods will create game_title, game_description
	it'll return game objects
	"""
	def post(self, request, format="json"):
		user = User.objects.get(id=self.request.user.id)
		game = Game.objects.get(id=request.data.get('game', None))
		game_description = request.data.get('game_description', None)
		game_title = request.data.get('game_title', None)
		# like_count = request.data.get('like_count', None)

		game_obj = Gamefeeds.objects.create(user=user, game=game,
								game_title=game_title,
								game_description=game_description)
		return Response(status=status.HTTP_200_OK)

	"""
	this method will update the game description
	"""
	def put(self, request, format="json"):
		user = User.objects.get(id=self.request.user.id)
		game = Game.objects.get(id=request.data.get('game', None))
		game_title = request.data.get('game_title', None)
		game_description = request.data.get('game_description', None)
		# like_count = request.data.get('like_count', None)

		try:
			game_obj = Gamefeeds.objects.get(user=user,game=game,
								game_title=game_title)
			if game_obj.game_description != game_description:
				game_obj.game_description = game_description
				game_obj.created_at=datetime.datetime.now()
				game_obj.save()
			else:
				game_obj.created_at=datetime.datetime.now()
				game_obj.save()
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)
