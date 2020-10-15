from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from AuthApp.models import MyUserAccount
from .models import *
from .serializers import *
import calendar
import time


# Create your views here.
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def allPosts(request):
    posts = Post.objects.filter(is_delete=False).order_by('-id')
    serializer = PostSerializer(posts, context={'request': request}, many=True)
    DictData = {}
    DictData['status'] = 'SUCCESS'
    DictData['response'] = serializer.data
    DictData['message'] = 'All Posts sent'
    return Response(serializer.data, status=200)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def myPosts(request):
    user = request.user
    posts = Post.objects.filter(created_by=user, is_delete=False).order_by('-id')
    serializer = PostSerializer(posts, context={'request': request}, many=True)
    DictData = {}
    DictData['status'] = 'SUCCESS'
    DictData['response'] = serializer.data
    DictData['message'] = 'All Posts sent'
    return Response(serializer.data, status=200)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getPostDetail(request):
    postId = request.data['postId']
    posts = Post.objects.get(id=postId, is_delete=False)
    DictData = {}
    if posts:
        serializer = PostSerializer(posts, context={'request': request})
        DictData['status'] = 'SUCCESS'
        DictData['response'] = serializer.data
        DictData['message'] = 'Posts sent'
        return Response(DictData, status=200)
    else:
        DictData['status'] = 'FAIL'
        DictData['response'] = ''
        DictData['message'] = 'Post Not Found'
        return Response(DictData, status=406)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createPost(request):
    user = request.user
    title = request.data['title']
    content = request.data['content']
    postImage = request.FILES['postImage']
    hashTag = request.data['hashTag']
    DictData = {}
    post = Post.objects.create(
        created_by=user,
        title=title,
        content=content,
        post_image=postImage,
        hash_tag=hashTag,
        created_on=calendar.timegm(time.gmtime())
    )
    if post:
        # serializer = PostSerializer(post)
        DictData['status'] = 'SUCCESS'
        DictData['response'] = '' # serializer.data
        DictData['message'] = 'Posts Created Successfully'
        return Response(DictData, status=200)
    else:
        DictData['status'] = 'FAIL'
        DictData['response'] = ''
        DictData['message'] = 'Post Create Request Failed'
        return Response(DictData, status=406)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deletePost(request):
    user = request.user
    postId = request.data['postId']
    DictData = {}
    obj = Post.objects.get(id=postId, created_by=user, is_delete=False)
    if obj:
        obj.is_delete = True
        obj.updated_on = calendar.timegm(time.gmtime())
        obj.save()
        DictData['status'] = 'SUCCESS'
        DictData['response'] = ''
        DictData['message'] = 'Post Deleted Successfully'
        return Response(DictData, status=200)
    else:
        DictData['status'] = 'FAIL'
        DictData['response'] = ''
        DictData['message'] = 'Post Not Delete'
        return Response(DictData, status=406)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def postLikeDislike(request):
    user = request.user
    postId = request.data['postId']
    userObj = MyUserAccount.objects.get(email=user, is_delete=False)
    liked = Post.objects.filter(id=postId, like=userObj, is_delete=False)
    postObj = Post.objects.get(id=postId)
    DictData = {}
    if liked:
        postObj.like.remove(userObj)
        postObj.save()
        totalLike = postObj.like.count()
        DictData['status'] = 'SUCCESS'
        DictData['response'] = {'like': False, 'total': totalLike}
        DictData['message'] = 'Post Disliked'
        return Response(DictData, status=200)
    else:
        postObj.like.add(userObj)
        postObj.save()
        totalLike = postObj.like.count()
        DictData['status'] = 'SUCCESS'
        DictData['response'] = {'like': True, 'total': totalLike}
        DictData['message'] = 'Post liked'
        return Response(DictData, status=200)

