from django.contrib import admin
from .models import *

class FollowUserAdmin(admin.ModelAdmin):
	list_display = ('follower','following','created_at',)

admin.site.register(FollowUser,FollowUserAdmin)