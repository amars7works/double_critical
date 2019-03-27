from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user','created_at','updated_at',)

class CountryAdmin(admin.ModelAdmin):
	list_display = ('country_name','country_code',)

class SocialLoginAdmin(admin.ModelAdmin):
	list_display = ('user', )

admin.site.register(Profile,ProfileAdmin)
admin.site.register(Country,CountryAdmin)
admin.site.register(State)
admin.site.register(SocialLogin,SocialLoginAdmin)
