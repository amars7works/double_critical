from django.contrib import admin
from .models import *

class GameAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at', 'updated_at',)

class GameExtendAdmin(admin.ModelAdmin):
	list_display = ('game', 'created_at', 'updated_at')

class FollowGameAdmin(admin.ModelAdmin):
	list_display = ('user','game','created_at',)

class RateGameAdmin(admin.ModelAdmin):
	list_display = ('user','game', 'game_rating', 'created_at',)

class GameCollectionAdmin(admin.ModelAdmin):
	list_display = ('user','game','created_at',)

class LikeGameAdmin(admin.ModelAdmin):
	list_display = ('user','game','game_like','created_at',)

admin.site.register(Game,GameAdmin)
admin.site.register(GameExtend,GameExtendAdmin)
admin.site.register(FollowGame,FollowGameAdmin)
admin.site.register(RateGame,RateGameAdmin)
admin.site.register(GameCollection,GameCollectionAdmin)
admin.site.register(LikeGame,LikeGameAdmin)
admin.site.register(Tags)
admin.site.register(GameCategory)
admin.site.register(GameTag)
admin.site.register(Designer)
admin.site.register(Artist)
admin.site.register(Publisher)
admin.site.register(Mechanism)
admin.site.register(GameGallery)
admin.site.register(GameFeed)
admin.site.register(LikeLog)
admin.site.register(SocialBase)
admin.site.register(GameComment)
admin.site.register(Gamefeeds)
