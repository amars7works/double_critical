# from elasticsearch_dsl.connections import connections
# from elasticsearch_dsl import DocType, Text, Date, Integer, Boolean #Document, Keyword, connections
# from elasticsearch.helpers import bulk
# from elasticsearch import Elasticsearch
# from . import models

# connections.create_connection()

# class GameIndex(DocType):
# 	name = Text()
# 	year_published = Date()
# 	minimum_players = Integer()
# 	maximum_players = Integer()
# 	mfg_suggested_ages = Text()
# 	minimum_playing_time = Text()
# 	maximum_playing_time = Text()
# 	designer = Text()
# 	artist = Text()
# 	publisher = Text()
# 	category = Text()
# 	mechanism = Text()
# 	views = Integer()
# 	like_count = Integer()
# 	game_status = Text()
# 	hotornot = Boolean()
# 	upc = Text()
# 	origin = Text()

# 	class Meta:
# 		index = 'game-index'

# def bulk_indexing():
# 	GameIndex.init()
# 	es = Elasticsearch()
# 	bulk(client=es, actions=(b.indexing() for b in models.Game.objects.all().iterator()))