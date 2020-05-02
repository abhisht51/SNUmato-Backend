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


#RESTAURANTS 

@api_view(["GET"])
def getAllRestaurants(request):
    cultural_data = []
    queryset = Restaurant.objects.all().values()
    return Response({"restaurants":list(queryset)})



#MENU 

@api_view(["GET"])
def getmenu(request):
    resutaurant_id = request.GET.get('restaurant_id')
    print(str(resutaurant_id) + " HEYLLLLLO")
    menu_items = Menu_item.objects.filter(restaurant=resutaurant_id)
    return Response({"restaurants":list(menu_items.values())})


#CURRENT ORDERS / CART 


@api_view(["POST"])
@permission_classes((IsAuthenticated, ))
def addtocart(request):
    user = get_object_or_404(User, email=request.user)
    restaurant_id = request.data.get('restaurant_id')
    item_id = request.data.get('item_id')
    quantity = request.data.get('quantity')    
    try:
        menu_item =  Menu_item.objects.get(restaurant=restaurant_id,id=item_id)
    except:
        return Response({
            "message":"Error No such item in the database"
        },status=status.HTTP_400_BAD_REQUEST)

    try :
        p = Current_order.objects.create(user=user,item_cost=menu_item.item_cost,
        item_quantity = quantity,item_name = menu_item.item_name,u_id=user.id,item_id=item_id)
        p.save()
    except:
        return Response({
            "message":"Error OOOOF"
        },status=status.HTTP_400_BAD_REQUEST)
    return Response({
         "message":"Item has been successfully added to the cart."
    },status=status.HTTP_202_ACCEPTED)

@api_view(["POST"])
@permission_classes((IsAuthenticated, ))
def updatecart(request):
    user = get_object_or_404(User, email=request.user)
    item_id = request.data.get('item_id')
    quantity = request.data.get('quantity')
    try :
        p = Current_order.objects.get(user=user,item_id=item_id)
        p.item_quantity = quantity
        p.save()
    except:
        return Response({
            "message":"Error OOOOF"
        },status=status.HTTP_400_BAD_REQUEST)
    return Response({
         "message":"Success. Item Quantity has been updated."
    },status=status.HTTP_202_ACCEPTED)

@api_view(["POST"])
@permission_classes((IsAuthenticated, ))
def deleteitem(request):
    user = get_object_or_404(User, email=request.user)
    item_id = request.data.get('item_id')
    try :
        p = Current_order.objects.get(user=user,item_id=item_id)       
        p.delete()               
    except:
        return Response({
            "message":"Error  No such item in the database OOF"
        },status=status.HTTP_400_BAD_REQUEST)
    return Response({
         "message":"Success. Item has been removed from the cart."
    },status=status.HTTP_202_ACCEPTED)


@api_view(["GET"])
@permission_classes((IsAuthenticated, ))
def cart(request):
    user = get_object_or_404(User, email=request.user)
    try :
        p = Current_order.objects.filter(user=user)
    except:
        return Response({
            "message":"Error : Cart is empty OOF"
        },status=status.HTTP_200_OK)


    totalcost = 0
    for i in p.values():
        totalcost = totalcost + int(i["item_cost"])*int(i["item_quantity"])
    return Response({
         "data":list(p.values()),
         "total_cost" : totalcost,
          "total_cost_gst": totalcost*(1.1),
           "delivery": 10,
           "final_cost": totalcost*(1.1) + 10,     
    },status=status.HTTP_202_ACCEPTED)

#PLACE ORDER 

@api_view(["POST"])
@permission_classes((IsAuthenticated, ))
def placeorder(request):
    user = get_object_or_404(User, email=request.user)
    address = request.data.get('address')
    payment_method = request.data.get('payment_method')

    Uuid = uuid.uuid4()
    uid = Uuid.hex[0:5]
    while(len(Orders.objects.filter(user=user,order_id=uid)) > 0):
        Uuid = uuid.uuid4()
        uid  = Uuid.hex[0:5]
    
    try :
        p = Current_order.objects.filter(user=user)
    except:
        return Response({
            "message":"Error : No orders placed  OOF"
        },status=status.HTTP_200_OK)

    totalcost = 0.00
    for i in p.values():
        totalcost = totalcost + int(i["item_cost"])*int(i["item_quantity"])
    totalcost = 10 + totalcost*1.1
    if(totalcost <= 0):
        raise ValueError
       
    order_details = json.dumps(list(p.values()))
        
    try:
        order = Orders.objects.create(user=user,uuid=Uuid,order_id=uid)
        order.order_description = order_details        
        order.total_amount = totalcost
        order.payment_method = payment_method   #TODO 
        p.delete()
        order.save()
    except:
        return Response({"message":"Unable to place order"})
    
    try:
        if address:
            user.address = address 
            user.save()
        else:
            raise ValueError
    except:
        return Response({
            "message":"Address could not be added"
        })        
    # p.delete()
    return Response({
         "message":"Your order has been placed successfully."
    },status=status.HTTP_200_OK)


# ORDER HISTORY  
@api_view(["GET"])
@permission_classes((IsAuthenticated, ))
def orderhistory(request):
    user = get_object_or_404(User, email=request.user)
    
    try:
        order = Orders.objects.filter(user=user).order_by('-date_time')[:5]
    except:
        return Response({"message":"Something is wrong :/"},status= status.HTTP_400_BAD_REQUEST)

    return Response(
        {
           "orders" : list(order.values()) 
        },
        status = status.HTTP_200_OK
    )


# USER INFO 


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
