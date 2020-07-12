from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate, login, logout
from .models import *


class MyUserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUserAccount
        fields = ['first_name', 'last_name', 'email']

    def validate(self, data):
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        email = data.get('email', '')
        password = data.get('password', '')
        date_of_birth = data.get('date_of_birth', '')
        if MyUserAccount.objects.filter(email=email).exists():
            message = 'Email is already exist'
            raise exceptions.ValidationError(message)
        else:
            user = MyUserAccount.objects.create_user(first_name, last_name, date_of_birth, email, password)
            data['user'] = user
        return data


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

    def validate(self, data):
        email = data.get('email', '')
        password = data.get('password', '')
        if email and password:
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    data['user'] = user
            else:
                raise exceptions.AuthenticationFailed()
        else:
            message = 'Must provide email and password'
            raise exceptions.ValidationError(message)
        return data


class MyUserAccountProfileSerializer(serializers.ModelSerializer):
    follower = serializers.IntegerField(source='followers.count', read_only=True)
    followed_by = MyUserAccountSerializer(source='followers', many=True)
    isFollow = serializers.SerializerMethodField('get_isFollowed')
    following = serializers.SerializerMethodField('get_followings')

    def get_isFollowed(self, obj):
        user = self.context['request'].user
        followerUser = MyUserAccount.objects.get(email=user, is_active=True, is_delete=False)
        return MyUserAccount.objects.filter(id=obj.id, followers=followerUser, is_active=True, is_delete=False).exists()

    def get_followings(self, obj):
        return MyUserAccount.objects.filter(followers=obj.id, is_active=True, is_delete=False).count()

    class Meta:
        model = MyUserAccount
        fields = ['id', 'follower', 'following', 'followed_by', 'isFollow', 'profile_picture', 'first_name',
                  'last_name', 'email', 'contact', 'profession', 'biography']
