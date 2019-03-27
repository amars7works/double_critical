from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from game.models import *
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.forms.models import model_to_dict

class Search(APIView):
	def get(self, request, format="json"):
		data = request.GET.get('data', None)
		 #filter(name__icontains=data).order_by('name')
		print (data)
		vector = SearchVector('name', weight='A') #+ SearchVector('category__category_name', weight='B')
		query = SearchQuery(data)
		game_qs = Game.objects.annotate(rank=SearchRank(
						vector, query)).filter(rank__gte=0.3).order_by('rank')
		print (game_qs, '----------------------')
		games = [game for game in game_qs.values()]

		return JsonResponse(games, safe=False)
