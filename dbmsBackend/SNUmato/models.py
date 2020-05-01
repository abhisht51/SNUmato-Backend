from django.db import models
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib import auth
# Create your models here.


class Restaurant(models.Model):
    restaurant_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=2,decimal_places=1)
    working_hours = models.CharField(max_length=100)
    cost_for_two = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=100,help_text='Contact Number of the restaurant owner',null=True)
    class Meta:
        db_table = 'Restaurant'
    def __str__(self):
        return self.name


class Menu_item(models.Model):
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)  # concept of 1:1 Foreign KEY TODO 
    item_name = models.CharField(max_length=100)

    item_category = models.CharField(max_length=100)
    item_description = models.TextField(default="") #TODO check before sending as a JSON 
    item_cost = models.PositiveIntegerField()

    CHOICES = (("Veg","Veg"),
                ("Non Veg","Non Veg"),
            )

    veg_nonVeg = models.CharField(max_length=100,null=True,choices=CHOICES) 
    
    class Meta:
        db_table = 'Menu_Item'
    def __str__(self):
        return self.item_name


class Orders(models.Model):                                      # db for displaying users past orders. 
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    order_id = models.PositiveIntegerField(null=False)
    u_id = models.PositiveIntegerField(null=False)
    date_time = models.DateTimeField(auto_now=True,null=True)
    order_description = models.CharField(max_length=1000)
    total_amount = models.DecimalField(max_digits=9,decimal_places=2)
    CHOICES = (("Cash On Delivery","COD"),
                ("Online-UPI","UPI"),
                ("Online-Paytm","PAYTM"),)
    payment_method = models.CharField(max_length=30,default='COD',choices=CHOICES)
    def __str__(self):
        return self.user.name + " " + self.order_id
    class Meta:
        db_table = 'Orders'

class Current_order(models.Model): 
    # TODO cart item funtion 
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item_cost = models.CharField(max_length=100)
    u_id = models.PositiveIntegerField(null=False)

    item_quantity = models.PositiveIntegerField()
    item_name = models.CharField(max_length=100)
    item_id = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'Current_order'
    def __str__(self):
        return self.item_name


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address!')

        if not password:
            raise ValueError('Users must have a password!')

        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.save(using = self._db)
        return user_obj

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password
        )
        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user      


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    active = models.BooleanField(default=True) # can log in
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    uuid=models.CharField(max_length=200, default="")
    created_at = models.DateTimeField(default=datetime.now)
    mobile_num = models.CharField(max_length=10,null=True)
     
    
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = [] #USERNAME_FIELD and Password required by default.

    objects = UserManager()

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active

    # # def save(self, *args, **kwargs):
    # #     self.subscription_end = date.today() + relativedelta(months=+self.subscription_period)
    # #     super(User, self).save(*args, **kwargs) # Call the "real" save() method.

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)


