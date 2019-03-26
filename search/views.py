from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from game.models import *
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.forms.models import model_to_dict

class Search(APIView):
	def get(self, request, format="json"):
		data = request.GET.get('data', None)
		game_qs = Game.objects.filter(name__icontains=data).order_by('name')#.annotate(
						# search=SearchVector('name'),
						# ).filter(search=SearchQuery('Lord'))
		# game = model_to_dict(game_qs)
		# print (game, '----------------------')
		games = [game for game in game_qs.values()]

		return JsonResponse(games, safe=False)
