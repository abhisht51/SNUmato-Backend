from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, JsonResponse
from SNUmato.models import User,Menu_item,Current_order,Orders,Restaurant
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
from rest_framework import status
from .serializers import cart_Serializers,menu_Serializers,restaurant_Serializer,orders_Serializers 
 




# Create your views here.
def test(request):
    return HttpResponse('Test chal rha') 





# @api_view(["POST"])
# def item_post(request):
#     item_name = request.data.get('item_name')
#     item_category = request.data.get('item_category')
#     item_description = request.data.get('item_description')
#     item_cost = request.data.get('item_cost')
#     veg_nonVeg = request.data.get('vegnonVeg')
#     #item = Menu_item.objects.create_user()



#RESTAURANTS 

@api_view(["GET"])
def getAllRestaurants(request):
    cultural_data = []
    queryset = Restaurant.objects.all().values()
    return JsonResponse({"restaurants":list(queryset)})



#MENU 

@api_view(["GET"])
def getmenu(request):
    resutaurant_id = request.GET.get('restaurant_id')
    print(str(resutaurant_id) + " HEYLLLLLO")
    menu_items = Menu_item.objects.filter(restaurant=resutaurant_id)
    return JsonResponse({"restaurants":list(menu_items.values())})


#CURRENT ORDERS / CART 


@api_view(["POST"])
@permission_classes((IsAuthenticated, ))
def addtocart(request):
    user = get_object_or_404(User, email=request.user)
    restaurant_id = request.data.get('restaurant_id')
    item_id = request.data.get('item_id')
    quantity = request.data.get('quantity')
    
    menu_item =  Menu_item.objects.get(restaurant=restaurant_id,id=item_id)
   
    p = Current_order.objects.create(user=user,item_cost=menu_item.item_cost,item_quantity =  quantity,item_name = menu_item.item_name,u_id=user.id)
    try :
        # p = Current_order.objects.create(user=user.id,item_cost=menu_item.item_cost,quantity =  quantity,item_name = menu_item.item_name )
        # p.user = user.id 
        # p.item_cost = menu_item.item_cost
        # p.quantity =  int(quantity)
        # p.item_name = menu_item.item_name 
        p.save()
    except:
        return Response({
            "message":"Error OOOOF"
        },status=status.HTTP_400_BAD_REQUEST)
    return Response({
         "message":"success"
    },status=status.HTTP_202_ACCEPTED)

@api_view(["POST"])
@permission_classes((IsAuthenticated, ))
def updatecart(request):
    user = get_object_or_404(User, email=request.user)
    password = request.data.get("password")
    user = authenticate(email=user.email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials', 'status': 'fail'})
    user.set_password(request.data.get('new_password'))
    user.save()
    return JsonResponse({'status': 'success'})

@api_view(["POST"])
@permission_classes((IsAuthenticated, ))
def deleteitem(request):
    user = get_object_or_404(User, email=request.user)
    password = request.data.get("password")
    user = authenticate(email=user.email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials', 'status': 'fail'})
    user.set_password(request.data.get('new_password'))
    user.save()
    return JsonResponse({'status': 'success'})





















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
    token = Token.objects.create(user=user)

    logged_in_user = User.objects.filter(email=user).values()[0]
    return JsonResponse({'status': 'success',
    'token': token.key, 
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
