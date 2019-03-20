from django.contrib import admin
from .models import *

class UGCAdmin(admin.ModelAdmin):
	list_display = ('user','game','ugc_title','like_count','created_at')

class UGCLikeAdmin(admin.ModelAdmin):
	list_display = ('user','ugc','like_type','created_at',)

class UGCCommentAdmin(admin.ModelAdmin):
	list_display = ('user','game','ugc','created_at','updated_at')

class UGCCommentLikeAdmin(admin.ModelAdmin):
	list_display = ('user','ugccomment','created_at',)

class UGCReportAdmin(admin.ModelAdmin):
	list_display = ('user','ugc','created_at','description')


admin.site.register(UGCReport,UGCReportAdmin)
admin.site.register(UGCLike,UGCLikeAdmin)
admin.site.register(UGCCommentLike,UGCCommentLikeAdmin)
admin.site.register(UGCComment, UGCCommentAdmin)
admin.site.register(UGC, UGCAdmin)