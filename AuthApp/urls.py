from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from AuthApp.views import *

app_name = "AuthApp"
urlpatterns = [

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
