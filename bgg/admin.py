from django.contrib import admin
from .models import *

class GameFollowAdmin(admin.ModelAdmin):
	list_display = ('user','game','created_at','updated_at')


class GameCommentAdmin(admin.ModelAdmin):
	list_display = ('user','game','created_at','updated_at')


class RateGameAdmin(admin.ModelAdmin):
	list_display = ('user','game','created_at','updated_at')


class CollectionAdmin(admin.ModelAdmin):
	list_display = ('user','game','created_at','updated_at')


class UGCCommentAdmin(admin.ModelAdmin):
	list_display = ('user','game','created_at','updated_at')

class UGCAdmin(admin.ModelAdmin):
	list_display = ('user','ugc_title','created_at','updated_at')


admin.site.register(Game)
admin.site.register(GameExtend)
admin.site.register(GameFollow,GameFollowAdmin)
admin.site.register(GameComment,GameCommentAdmin)
admin.site.register(RateGame,RateGameAdmin)
admin.site.register(Collection,CollectionAdmin)
admin.site.register(UGCComment, UGCCommentAdmin)
admin.site.register(UGC, UGCAdmin)
