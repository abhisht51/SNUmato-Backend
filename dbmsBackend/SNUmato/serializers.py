from rest_framework import serializers

from .models import Restaurant,Current_order,Orders,Menu_item,User

class restaurant_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class user_Serializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','address','mobile_num']

class cart_Serializers(serializers.ModelSerializer):
    class Meta:
        model = Current_order
        fields = '__all__'

class orders_Serializers(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class menu_Serializers(serializers.ModelSerializer):
    class Meta:
        model = Menu_item
        fields = '__all__'
