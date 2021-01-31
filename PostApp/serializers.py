from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from AuthApp.serializers import MyUserAccountSerializer, MyUserAccountProfileSerializer
from AuthApp.models import MyUserAccount
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    user_id = SerializerMethodField()
    post_id = SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['user_id', 'post_id', 'content', 'created_on']


class PostSerializer(serializers.ModelSerializer):
    created_by = MyUserAccountProfileSerializer()
    likes = serializers.IntegerField(source='like.count', read_only=True)
    liked_by = MyUserAccountSerializer(source='like', many=True)
    isLiked = serializers.SerializerMethodField('get_isLiked')
    # total_comments = serializers.IntegerField(source='comment.count', read_only=True)
    # comment = CommentSerializer(source='comment', many=True)

    def get_isLiked(self, obj):
        user = self.context['request'].user
        return Post.objects.filter(id=obj.id, like=user).exists()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'post_image', 'likes', 'liked_by', 'isLiked',
                  'created_on', 'created_by']
