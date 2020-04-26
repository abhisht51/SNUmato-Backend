from django.contrib import admin

# Register your models here.
from .models import Current_order,Orders,Menu_item,Restaurant,User

admin.site.register(Restaurant)
admin.site.register(Menu_item)
admin.site.register(Orders)
admin.site.register(Current_order)
admin.site.register(User)

