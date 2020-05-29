from django.contrib import admin
from .models import *


# Register your models here.
class MyUserAccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'created_on',)
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ('email',)


admin.site.register(MyUserAccount, MyUserAccountAdmin)

admin.site.register(emailHandler)