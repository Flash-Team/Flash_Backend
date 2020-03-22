from django.contrib import admin
from flash.order.models import Order, OrderedProduct


# Need to add filial to list_display
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'client', 'courier', 'created_at')


@admin.register(OrderedProduct)
class OrderedProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'count', 'order')
