from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from AuthApp.views import *

app_name = "AuthApp"
urlpatterns = [
    path('register/', createUserAccount, name='createUserAccount'),
    path('verification/', emailVerification, name='emailVerification'),
    path('userdata/', getEmailById, name='getEmailById'),
    path('login/', logInUser, name='logInUser'),
    path('logout/', logOutUser, name='logOutUser'),
    path('profile/', getCurrentUserProfile, name='getCurrentUserProfile'),
    path('edit-profile/', editUserProfile, name='editUserProfile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
