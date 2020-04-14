from rest_framework import serializers

from flash.organization.serializers import OrganizationSerializer
from flash.product.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)


class Product2Serializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'logo', 'price', 'organization', 'category',)
