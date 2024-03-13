from django.contrib import admin
from .models import Customer,Car,Cart,ContactUsMessage,Order
# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display= ['id','user','name','address','city','state','pincode']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display= ['id','name','category','small_description','description','selling_price','discounted_price']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display= ['id','user','product','quantity']

@admin.register(ContactUsMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display= ['id','name','email','subject','message','created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display= ['id','user','car','quantity','order_at','status']