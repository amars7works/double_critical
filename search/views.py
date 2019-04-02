from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from game.models import *
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.forms.models import model_to_dict

class Search(APIView):
	def get(self, request, format="json"):
		text = request.GET.get('text', None)
		vector = SearchVector('name') + SearchVector('category__category_name') + \
						SearchVector('tag__tag_name')
		query = SearchQuery(text)
		# game_qs = Game.objects.annotate(rank=SearchRank(
						# vector, query)).filter(rank__gte=0.3).order_by('rank')
		game_qs = Game.objects.annotate(search=vector).filter(search=query)
		response = [game for game in game_qs.values()]

		return JsonResponse(response, safe=False)
