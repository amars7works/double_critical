from django.http import JsonResponse
from rest_framework.views import APIView

from game.models import *
from dc.views import *
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank

class Search(APIView):
	def get(self, request, format="json"):
		text = request.GET.get('text', None)
		vector = SearchVector('name', weight='D') + SearchVector('category__category_name', weight='B')
		query = SearchQuery(text)
		game_qs = Game.objects.annotate(rank=SearchRank(
						vector, query)).filter(rank__gte=0.02).order_by('rank')
		# game_qs = Game.objects.annotate(search=vector).filter(search=query)

		ids = []
		for game in game_qs.values():
			ids.append(game['id'])

		vector_1 = SearchVector('tag__tag_name', weight='B')
		# game_tags = GameTag.objects.annotate(search=vector_1).filter(search=query)
		game_tags = GameTag.objects.annotate(rank=SearchRank(
						vector_1, query)).filter(rank__gte=0.02).order_by('rank')
		for game_tag in game_tags:
			if game_tag.game.id not in ids:
				ids.append(game_tag.game.id)

		games = [gameobj for gameobj in Game.objects.filter(id__in=ids).values()]

		return JsonResponse(obj_to_dict(games), safe=False)
