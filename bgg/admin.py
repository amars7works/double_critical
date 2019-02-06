from django.contrib import admin
from .models import *

class GameFollowAdmin(admin.ModelAdmin):
	list_display = ('user','game','created_at',)


class RateGameAdmin(admin.ModelAdmin):
	list_display = ('user','game','created_at',)


class GameCollectionAdmin(admin.ModelAdmin):
	list_display = ('user','game','created_at',)


class UGCAdmin(admin.ModelAdmin):
	list_display = ('user','ugc_title','created_at',)


# class UGCLikeAdmin(admin.ModelAdmin):
# 	list_display = ('user','ugc_title','created_at',)


class UGCCommentAdmin(admin.ModelAdmin):
	list_display = ('user','game','created_at','updated_at')


# class UGCCommentLike(admin.ModelAdmin):
# 	list_display = ('user','ugc_title','created_at',)


class FollowUserAdmin(admin.ModelAdmin):
	list_display = ('follower','following','created_at',)



admin.site.register(Game)
admin.site.register(GameExtend)
admin.site.register(GameFollow,GameFollowAdmin)
admin.site.register(RateGame,RateGameAdmin)
admin.site.register(GameCollection,GameCollectionAdmin)
admin.site.register(UGCComment, UGCCommentAdmin)
admin.site.register(UGC, UGCAdmin)
admin.site.register(FollowUser,FollowUserAdmin)
admin.site.register(UGCLike)
admin.site.register(UGCCommentLike)
