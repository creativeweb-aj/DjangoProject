from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate, login, logout
from .models import *


class MyUserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUserAccount
        fields = ['id', 'first_name', 'last_name', 'email', 'date_of_birth']

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


