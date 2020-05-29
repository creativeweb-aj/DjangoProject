from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from AuthApp.views import *

app_name = "AuthApp"
urlpatterns = [
    path('', index, name='emailThread'),
    path('register/', createUserAccount, name='createUserAccount'),
    path('verification/', emailVerification, name='emailVerification'),
    path('login/', logInUser, name='logInUser'),
    path('logout/', logOutUser, name='logOutUser'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
