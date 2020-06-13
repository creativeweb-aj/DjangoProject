from django.contrib import admin
from .models import *

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_by', 'created_on',)
    search_fields = ['title', 'content', 'hash_tag']
    list_filter = ('title', 'created_by',)

admin.site.register(Post, PostAdmin)

admin.site.register(Like)
