from django.contrib import admin
from flash.order.models import Order, OrderedProduct


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'filial', 'client', 'courier', 'created_at', 'delivered',)


@admin.register(OrderedProduct)
class OrderedProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'count', 'order')
