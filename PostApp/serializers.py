from rest_framework import serializers, exceptions
from .models import *


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'post_image', 'hash_tag', 'created_on', 'created_by']
