from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_by', 'created_on',)
    search_fields = ['title', 'content', 'hash_tag']
    list_filter = ('title', 'created_by',)


admin.site.register(Post, PostAdmin)


class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'post_id',)


admin.site.register(Like, PostLikeAdmin)


class PostCommentAdmin(MPTTModelAdmin):
    list_display = ('user_id', 'post_id', 'content', 'created_on',)


admin.site.register(Comment, PostCommentAdmin)
