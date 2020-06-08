from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.decorators import parser_classes, api_view
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.core.files.storage import FileSystemStorage
from .models import *
from .serializers import *
from .email import *
from .crypto import *


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
            emailService.saveEmail(user)
            serializer = MyUserAccountSerializer(user)
            # token = Token.objects.get(user_id=user)
            key = encrypt(user.id)
            DictData['status'] = 'SUCCESS'
            DictData['keyId'] = key
            DictData['response'] = serializer.data
            DictData['message'] = 'User created, Please verify email to login'
        return Response(DictData, status=201)


@api_view(['POST'])
def getEmailById(request):
    if request.method == 'POST':
        userId = request.data['userId']
        key = decrypt(userId)
        user = MyUserAccount.objects.get(id=key)
        DictData = {}
        if user:
            serializer = MyUserAccountSerializer(user)
            print('serializer email data ::::', serializer.data['email'])
            DictData['status'] = 'SUCCESS'
            DictData['response'] = serializer.data['email']
            DictData['message'] = 'User email send'
            return Response(DictData, status=200)
        else:
            DictData['status'] = 'FAIL'
            DictData['response'] = ''
            DictData['message'] = 'User email not found'
            return Response(DictData, status=404)


@api_view(['POST'])
def emailVerification(request):
    if request.method == 'POST':
        print(request.data)
        emailId = request.data['emailId']
        otp = request.data['otp']
        currentTime = calendar.timegm(time.gmtime())
        DictData = {}
        if emailId and otp:
            emailData = emailHandler.objects.get(email_id=emailId, is_sent=True, is_verify=False)
            print('email data from table :: ', emailData)
            print('email data from table is expiry :: ', emailData.is_expiry)
            expiredDate = emailData.is_expiry - currentTime
            expiredDate = expiredDate / 60
            print('expired date :: ', expiredDate)
            if int(expiredDate) < 1440:
                if emailData.token == int(otp):
                    emailData.is_verify = True
                    emailData.updated_on = calendar.timegm(time.gmtime())
                    emailData.save()
                    userData = MyUserAccount.objects.get(email=emailId)
                    userData.is_active = True
                    userData.updated_on = calendar.timegm(time.gmtime())
                    userData.save()
                    DictData['status'] = 'SUCCESS'
                    DictData['response'] = ''
                    DictData['message'] = 'Email verified successfully'
                    return Response(DictData, status=200)
                else:
                    emailData.updated_on = calendar.timegm(time.gmtime())
                    emailData.save()
                    DictData['status'] = 'FAIL'
                    DictData['response'] = ''
                    DictData['message'] = 'Please enter correct OTP'
                    return Response(DictData, status=203)
            else:
                emailData.updated_on = calendar.timegm(time.gmtime())
                emailData.save()
                DictData['status'] = 'FAIL'
                DictData['response'] = ''
                DictData['message'] = 'OTP is expired'
                return Response(DictData, status=406)
        else:
            DictData['status'] = 'FAIL'
            DictData['response'] = ''
            DictData['message'] = 'Please enter OTP then send'
            return Response(DictData, status=406)


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


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def logOutUser(request):
    logout(request)
    DictData = {'status': 'SUCCESS', 'response': '', 'message': 'User logout successfully'}
    return Response(DictData, status=200)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getCurrentUserProfile(request):
    user = request.user
    print('user ::', user)
    obj = MyUserAccount.objects.get(email=user)
    DictData = {}
    if obj:
        serializer = MyUserAccountProfileSerializer(obj)
        DictData['status'] = 'SUCCESS'
        DictData['response'] = serializer.data
        DictData['message'] = 'User data send'
        return Response(DictData, status=200)
    else:
        DictData['status'] = 'FAIL'
        DictData['response'] = ''
        DictData['message'] = 'User data not found'
        return Response(DictData, status=406)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def editUserProfile(request):
    user = request.user
    firstName = request.data['firstName']
    lastName = request.data['lastName']
    profileChange = request.data['profileChange']
    if profileChange == 'True':
        profilePic = request.FILES['profilePic']
    profession = request.data['profession']
    bio = request.data['bio']
    contact = request.data['contact']
    obj = MyUserAccount.objects.get(email=user)
    print('obj :::', obj)
    DictData = {}
    if obj:
        print('obj first name ::', obj.first_name)
        obj.first_name = firstName
        obj.last_name = lastName
        obj.profession = profession
        obj.biography = bio
        obj.contact = contact
        if profileChange == 'True':
            obj.profile_picture = profilePic
        obj.updated_on = calendar.timegm(time.gmtime())
        obj.save()
        DictData['status'] = 'SUCCESS'
        DictData['response'] = ''  # serializer.data
        DictData['message'] = 'User profile updated'
        return Response(DictData, status=200)
    else:
        DictData['status'] = 'FAIL'
        DictData['response'] = ''
        DictData['message'] = 'User profile not updated'
        return Response(DictData, status=406)