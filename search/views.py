from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from game.models import *


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
