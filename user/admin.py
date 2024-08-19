from django.contrib import admin

# Register your models here.
from user.models import UserProfile
from .models import  SubscribedUsers
class SubscribedUsersAdmin(admin.ModelAdmin):
    list_display = ('email','created_date')


admin.site.register(SubscribedUsers, SubscribedUsersAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name','usertype','address','phone','city','country','image_tag']

admin.site.register(UserProfile,UserProfileAdmin)