from rest_framework import serializers, exceptions
from AuthApp.serializers import MyUserAccountSerializer, MyUserAccountProfileSerializer
from AuthApp.models import MyUserAccount
from .models import *


class PostSerializer(serializers.ModelSerializer):
    created_by = MyUserAccountProfileSerializer()
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'post_image', 'hash_tag', 'created_on', 'created_by']
