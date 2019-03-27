import datetime
import json
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User


class Ugc(APIView):
	def get(self, request, format="json"):
		game_obj = Game.objects.get(id=request.GET.get('game', None))
		# response = {}
		ugc_obj = UGC.objects.filter(game__name=game_obj.name).latest('created_at')
		ugc_comments = UGCComment.objects.filter(ugc__ugc_title=ugc_obj.ugc_title)
		# response[ugc_obj.ugc_title] = {}
		# response[ugc_obj.ugc_title].update(user=ugc_obj.user.username)
		# response[ugc_obj.ugc_title].update(comments_count=ugc_comment.count())
		response = [ugc_comment for ugc_comment in ugc_comments.values()]

		return JsonResponse(response, safe=False)

	def post(self, request, format="json"):
		user = User.objects.get(id=request.data.get('user', None))
		game = Game.objects.get(id=request.GET.get('game', None))
		ugc_title = request.data.get('ugc_title', None)
		like_count = request.data.get('like_count', None)

		ugc_obj = UGC.objects.create(user=user, game=game,
								ugc_title=ugc_title,
								like_count=like_count)
		return Response(status=status.HTTP_200_OK)

	def put(self, request, format="json"):
		user = User.objects.get(id=request.data.get('user', None))
		game = Game.objects.get(id=request.GET.get('game', None))
		ugc_title = request.data.get('ugc_title', None)
		like_count = request.data.get('like_count', None)

		try:
			ugc_obj = UGC.objects.get(user=user,game=game,
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
		# response = {}
		ugc = UGC.objects.get(id=request.GET.get('ugc', None))
		game = Game.objects.get(id=request.GET.get('game', None))
		
		ugc_comments = UGCComment.objects.filter(game__name=game.name,
								ugc__ugc_title=ugc.ugc_title
								).order_by('-created_at')
		response = [ugc_comment for ugc_comment in ugc_comments.values()]

		# for comment in ugc_comments:
		# 	comment_dict = model_to_dict(comment)
		# 	response[comment.game.name] = {}
		# 	response[comment.game.name].update(user__username=comment.user.username)
		# 	response[comment.game.name].update(ugc__ugc_title=comment.ugc.ugc_title)
		# 	response[comment.game.name].update(ugc_comment=comment.ugc_comment)
		# 	response[comment.game.name].update(id=comment.id)
		return JsonResponse(response, safe=False)

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

		ugc = UGC.objects.get(id=request.data.get('ugc', None))
		game = Game.objects.get(id=request.data.get('game', None))

		ugc_comment_like = request.data.get('ugc_comment_like', None)

		if ugc_comment_like == 'True':
			ugc_comment_like_obj = UGCCommentLike.objects.create(user=user,
									ugc_comment=ugc_comment, ugc=ugc, game=game)
			return Response(status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)

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

class UGCReportView(APIView):
	def post(self,request,format="json"):
		user = User.objects.get(id=request.data.get('user', None))
		ugc = UGC.objects.get(id=request.data.get('ugc', None))
		description = request.data.get('description', None)
		ugc_report = UGCReport.objects.create(user=user,ugc=ugc, description=description)
		return Response(status=status.HTTP_200_OK)
