from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, JsonResponse
from SNUmato.models import User
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
import json
import uuid





# Create your views here.
def test(request):
    return HttpResponse('Test chal rha') 







#USER INFO 

@api_view(["POST"])
def register(request):
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    mobile_num = request.data.get('mobile_num')
    uid = uuid.uuid4().hex[0:5]

    while(len(User.objects.filter(uuid=uid)) > 0):
        uid = uuid.uuid4().hex[0:5]
        
    user = User.objects.create_user(email=email, password=password)
    user.first_name = first_name
    user.last_name = last_name
    user.mobile_num = mobile_num
    user.save()

    # Generate Token for user
    # token = Token.objects.create(user=user)

    logged_in_user = User.objects.filter(email=user).values()[0]
    return JsonResponse({'status': 'success',
    # 'token': token.key, 
     'user_data': {
        'email': logged_in_user.get('email'),
        'first_name': logged_in_user.get('first_name'),
        'last_name': logged_in_user.get('last_name'),
        'mobile_num': logged_in_user.get('mobile_num'),
    }})




@api_view(["POST"])
@permission_classes((AllowAny,))
def Login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(email=email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials', 'status': 'fail'})
    token, _ = Token.objects.get_or_create(user=user)

    logged_in_user = User.objects.filter(email=user).values()[0]

    return Response({'token': token.key, 'status': 'success', 'user_data': {
        'email': logged_in_user.get('email'),
        'first_name': logged_in_user.get('first_name'),
        'last_name': logged_in_user.get('last_name'),
        'mobile_num': logged_in_user.get('mobile_num'),
    }})


@api_view(["POST"])
@permission_classes((IsAuthenticated, ))
def changePassword(request):
    user = get_object_or_404(User, email=request.user)
    password = request.data.get("password")
    user = authenticate(email=user.email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials', 'status': 'fail'})
    user.set_password(request.data.get('new_password'))
    user.save()
    return JsonResponse({'status': 'success'})


@api_view(["GET"])
@permission_classes((IsAuthenticated, ))
def verifyUser(request):
    user = get_object_or_404(User, email=request.user)

    user = User.objects.filter(email=request.user).values()[0]

    return Response({
        'status': 'success', 
        'user_data': {
        'email': user.get('email'),
        "uuid" : user.get("uuid"),
        'first_name': user.get('first_name'),
        'last_name': user.get('last_name'),
        'mobile_num': user.get('mobile_num'),
    }})
