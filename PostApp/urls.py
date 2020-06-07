from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from PostApp.views import *

app_name = "PostApp"
urlpatterns = [

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
