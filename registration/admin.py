from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user','created_at','updated_at')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Country)
admin.site.register(State)
