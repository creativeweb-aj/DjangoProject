from rest_framework import serializers, exceptions
from AuthApp.serializers import MyUserAccountSerializer, MyUserAccountProfileSerializer
from AuthApp.models import MyUserAccount
import json
from .models import *


class PostSerializer(serializers.ModelSerializer):
    created_by = MyUserAccountProfileSerializer()
    likes = serializers.IntegerField(source='like.count', read_only=True)
    liked_by = serializers.CharField(source='like.all', read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'post_image', 'likes', 'liked_by', 'hash_tag', 'created_on', 'created_by']
