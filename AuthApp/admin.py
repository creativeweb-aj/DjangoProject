from django.contrib import admin
from .models import *


# Register your models here.
class MyUserAccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'created_on',)
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ('email',)


admin.site.register(MyUserAccount, MyUserAccountAdmin)


class EmailAdmin(admin.ModelAdmin):
    list_display = ('email_id', 'subject', 'token', 'is_verify', 'sent_on', 'user')
    search_fields = ['email_id', 'subject']
    list_filter = ('email_id',)


admin.site.register(emailHandler, EmailAdmin)


# class FollowAdmin(admin.ModelAdmin):
#     list_display = ('follower', 'following')
#     search_fields = ['follower', 'following']
#     list_filter = ('follower',)
#
#
# admin.site.register(Follow, FollowAdmin)
