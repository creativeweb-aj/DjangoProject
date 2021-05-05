from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from AuthApp.serializers import MyUserAccountSerializer, MyUserAccountProfileSerializer
from AuthApp.models import MyUserAccount
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user_id', 'post_id', 'parent', 'content', 'created_on']


class PostSerializer(serializers.ModelSerializer):
    created_by = MyUserAccountProfileSerializer()
    likes = serializers.IntegerField(source='like.count', read_only=True)
    liked_by = MyUserAccountSerializer(source='like', many=True)
    isLiked = serializers.SerializerMethodField('get_isLiked')
    total_comments = serializers.SerializerMethodField('get_total_comment_count')
    comment = serializers.SerializerMethodField('get_comments')

    def get_isLiked(self, obj):
        user = self.context['request'].user
        return Post.objects.filter(id=obj.id, like=user).exists()

    def get_comments(self, obj):
        user = self.context['request'].user
        request = self.context['request']
        comments = Comment.objects.filter(post_id=obj.id, user_id=user)
        data_obj = CommentSerializer(comments, context={'request': request}, many=True)
        return data_obj.data

    def get_total_comment_count(self, obj):
        user = self.context['request'].user
        comments = Comment.objects.filter(post_id=obj.id, user_id=user).count()
        return comments

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'post_image', 'likes', 'liked_by', 'isLiked', 'comment', 'total_comments',
                  'created_on', 'created_by']
