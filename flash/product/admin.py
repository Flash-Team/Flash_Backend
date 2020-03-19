from django.contrib import admin
from flash.product.models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

#Deleted list_display[4] which is 'category'
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rating', 'price', 'category',)
