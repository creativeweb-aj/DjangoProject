from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
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
            status_code = 401
        elif MyUserAccount.objects.filter(email=email).exists():
            DictData['status'] = 'FAIL'
            DictData['response'] = ''
            DictData['message'] = 'Email is already exist'
            status_code = 409
        else:
            user = MyUserAccount.objects.create_user(first_name, last_name, date_of_birth, email, password)
            emailService = emailSendService()
            emailService.saveEmail(user)
            serializer = MyUserAccountSerializer(user)
            DictData['status'] = 'SUCCESS'
            DictData['response'] = {}
            DictData['response']['data'] = serializer.data
            DictData['message'] = 'User created, Please verify email to login'
            status_code = 201
        return Response(DictData, status=status_code)


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
        uuid = request.data['uuid']
        DictData = {}
        query = emailHandler.objects.filter(uuid=uuid, is_sent=True, is_verify=False).exists()
        if query:
            emailData = emailHandler.objects.get(uuid=uuid, is_sent=True, is_verify=False)
            print('email data ::', emailData)
            expiredDate = emailData.is_expiry - calendar.timegm(time.gmtime())
            expiredDate = expiredDate / 60
            if int(expiredDate) < 1440:
                emailId = emailData.email_id
                emailData.is_verify = True
                emailData.updated_on = calendar.timegm(time.gmtime())
                emailData.save()
                userData = MyUserAccount.objects.get(email=emailId)
                # userData.is_active = True
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
                DictData['message'] = 'Email link is expired'
                return Response(DictData, status=410)
        else:
            DictData['status'] = 'FAIL'
            DictData['response'] = ''
            DictData['message'] = 'Email already verified'
            return Response(DictData, status=409)


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
        DictData['response']['token'] = token.key
        DictData['response']['userId'] = user.id
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
    obj = MyUserAccount.objects.get(email=user, is_active=True, is_delete=False)
    DictData = {}
    if obj:
        serializer = MyUserAccountProfileSerializer(obj, context={'request': request})
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
def getUserProfile(request):
    user = request.user
    userId = request.data['userId']
    obj = MyUserAccount.objects.get(id=userId, is_active=True, is_delete=False)
    DictData = {}
    if user == obj:
        currentUser = True
    else:
        currentUser = False
    if obj:
        serializer = MyUserAccountProfileSerializer(obj, context={'request': request})
        DictData['status'] = 'SUCCESS'
        DictData['response'] = {}
        DictData['response']['data'] = serializer.data
        DictData['response']['currentUser'] = currentUser
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
def followUser(request):
    user = request.user
    userId = request.data['userId']
    followerUser = MyUserAccount.objects.get(email=user, is_active=True, is_delete=False)
    DictData = {}
    follow = MyUserAccount.objects.filter(id=userId, followers=followerUser, is_active=True, is_delete=False).exists()
    if follow:
        follow = MyUserAccount.objects.get(id=userId)
        follow.followers.remove(followerUser)
        serializer = MyUserAccountProfileSerializer(follow, context={'request': request})
        DictData['status'] = 'SUCCESS'
        DictData['response'] = serializer.data
        DictData['message'] = 'User Unfollowed'
        return Response(DictData, status=200)
    else:
        follow = MyUserAccount.objects.get(id=userId)
        follow.followers.add(followerUser)
        serializer = MyUserAccountProfileSerializer(follow, context={'request': request})
        DictData['status'] = 'SUCCESS'
        DictData['response'] = serializer.data
        DictData['message'] = 'User Followed'
        return Response(DictData, status=200)


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
    # profession = request.data['profession']
    bio = request.data['bio']
    # contact = request.data['contact']
    obj = MyUserAccount.objects.get(email=user, is_delete=False)
    print('obj :::', obj)
    DictData = {}
    if obj:
        print('obj first name ::', obj.first_name)
        obj.first_name = firstName
        obj.last_name = lastName
        # obj.profession = profession
        obj.biography = bio
        # obj.contact = contact
        if profileChange == 'True':
            obj.profile_picture = profilePic
        obj.updated_on = calendar.timegm(time.gmtime())
        obj.save()
        userObj = MyUserAccount.objects.get(email=user, is_delete=False)
        serializer = MyUserAccountProfileSerializer(userObj, context={'request': request})
        DictData['status'] = 'SUCCESS'
        DictData['data'] = serializer.data
        DictData['message'] = 'User profile updated'
        return Response(DictData, status=200)
    else:
        DictData['status'] = 'FAIL'
        DictData['data'] = ''
        DictData['message'] = 'User profile not updated'
        return Response(DictData, status=406)
