from django.contrib import admin
from .models import *

class GameAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at', 'updated_at',)

class GameExtendAdmin(admin.ModelAdmin):
	list_display = ('game', 'created_at', 'updated_at')

class FollowGameAdmin(admin.ModelAdmin):
	list_display = ('user','game','created_at',)


class RateGameAdmin(admin.ModelAdmin):
	list_display = ('user','game','created_at',)


class GameCollectionAdmin(admin.ModelAdmin):
	list_display = ('user','game','created_at',)


class UGCAdmin(admin.ModelAdmin):
	list_display = ('user','ugc_title','like_count','created_at',)


class UGCLikeAdmin(admin.ModelAdmin):
	list_display = ('user','ugc','like_type','created_at',)


class UGCCommentAdmin(admin.ModelAdmin):
	list_display = ('user','game','ugc','created_at','updated_at')


class UGCCommentLikeAdmin(admin.ModelAdmin):
	list_display = ('user','ugc_comment','created_at',)


class FollowUserAdmin(admin.ModelAdmin):
	list_display = ('follower','following','created_at',)

class LikeGameAdmin(admin.ModelAdmin):
	list_display = ('user','game','created_at',)


admin.site.register(Game,GameAdmin)
admin.site.register(GameExtend,GameExtendAdmin)
admin.site.register(FollowGame,FollowGameAdmin)
admin.site.register(RateGame,RateGameAdmin)
admin.site.register(GameCollection,GameCollectionAdmin)
admin.site.register(UGCComment, UGCCommentAdmin)
admin.site.register(UGC, UGCAdmin)
admin.site.register(FollowUser,FollowUserAdmin)
admin.site.register(UGCLike,UGCLikeAdmin)
admin.site.register(UGCCommentLike,UGCCommentLikeAdmin)
admin.site.register(LikeGame,LikeGameAdmin)