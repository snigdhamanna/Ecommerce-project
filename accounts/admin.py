from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import *
# Register your models here.
from django.contrib.admin import ModelAdmin 

from django.utils.html import format_html

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class ProfileAdmin(ModelAdmin):
    
    def profilepic(self , object):
        return format_html('<img src="{}" width="30" style=" border-radious"50%; ">'.format(object.profile_picture.url))
     
    profilepic.short_description ='Profile Picture'
    list_display = ('profilepic','user', 'city', 'state', 'country')
    


    
admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, ProfileAdmin)