from django.contrib import admin
from flash.product.models import Product, Category, Organization, Filial


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rating', 'manager',)


@admin.register(Filial)
class FilialAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'organization',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rating', 'price', 'organization', 'category',)
