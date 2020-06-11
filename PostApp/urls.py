from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from PostApp.views import *

app_name = "PostApp"
urlpatterns = [
    path('posts', allPosts, name='allPosts'),
    path('post-detail', getPostDetail, name='getPostDetail'),
    path('create-post', createPost, name='createPost'),
    path('delete-post', deletePost, name='deletePost'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
