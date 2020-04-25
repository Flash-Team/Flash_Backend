from django.contrib import admin

from flash.product.models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'logo', 'rating', 'price', 'organization', 'category',)
    search_fields = ('name', 'rating', 'price', 'organization', 'category')
