from rest_framework import serializers, exceptions
from AuthApp.serializers import MyUserAccountSerializer, MyUserAccountProfileSerializer
from AuthApp.models import MyUserAccount
import json
from .models import *


class PostSerializer(serializers.ModelSerializer):
    created_by = MyUserAccountProfileSerializer()
    likes = serializers.IntegerField(source='like.count', read_only=True)
    liked_by = MyUserAccountSerializer(source='like', many=True)
    isLiked = serializers.SerializerMethodField('get_isLiked')

    def get_isLiked(self, obj):
        user = self.context['request'].user
        return Post.objects.filter(id=obj.id, like=user).exists()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'post_image', 'likes', 'liked_by', 'isLiked', 'hash_tag',
                  'created_on', 'created_by']


class testProfileSerializer(serializers.ModelSerializer):
    post = PostSerializer(many=True)

    class Meta:
        model = MyUserAccount
        fields = ['id', 'first_name', 'email', 'post']
