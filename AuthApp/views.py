from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.decorators import parser_classes, api_view
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .models import *
from .serializers import *
from .email import *


def index(request):
    import threading
    obj = emailSendService()
    t = threading.Thread(target=obj.getEmailData, args=(), kwargs={})
    print("process started")
    t.setDaemon(True)
    t.start()
    return HttpResponse("main thread content")

@api_view(['POST'])
def createUserAccount(request):
    if request.method == 'POST':
        DictData = {}
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        email = request.data['email']
        password = request.data['password']
        password2 = request.data['password2']
        date_of_birth = request.data['date_of_birth']
        if password != password2:
            DictData['status'] = 'FAIL'
            DictData['response'] = ''
            DictData['message'] = 'Password must match'
        elif MyUserAccount.objects.filter(email=email).exists():
            DictData['status'] = 'FAIL'
            DictData['response'] = ''
            DictData['message'] = 'Email is already exist'
        else:
            user = MyUserAccount.objects.create_user(first_name, last_name, date_of_birth, email, password)
            emailService = emailSendService()
            is_save = emailService.saveEmail(user)
            if is_save:
                serializer = MyUserAccountSerializer(user)
                token = Token.objects.get(user_id=user)
                DictData['status'] = 'SUCCESS'
                DictData['response'] = serializer.data
                DictData['response']['token'] = token.key
                DictData['message'] = 'User created successfully'
            else:
                DictData['status'] = 'FAIL'
                DictData['response'] = ''
                DictData['message'] = 'Email is not sent'
        return Response(DictData, status=201)


@api_view(['POST'])
def emailVerification(request):
    pass


@api_view(['POST'])
def logInUser(request):
    if request.method == 'POST':
        DictData = {}
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        DictData['status'] = 'SUCCESS'
        DictData['response'] = {}
        DictData['token'] = token.key
        DictData['message'] = 'Login successfully'
        return Response(DictData, status=200)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def logOutUser(request):
    logout(request)
    DictData = {'status': 'SUCCESS', 'response': '', 'message': 'User logout successfully'}
    return Response(DictData, status=200)
