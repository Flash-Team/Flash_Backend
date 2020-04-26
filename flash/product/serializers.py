from rest_framework import serializers

from flash.product.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name',)

    def validate_name(self, value):
        if any(x in value for x in ['%', '&', '$', '^']):
            raise serializers.ValidationError('invalid character in name field')
        return value


class NestedProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'logo', 'name', 'description', 'price', 'rating', 'organization', )

    def validate_name(self, value):
        if any(x in value for x in ['%', '&', '$', '^']):
            raise serializers.ValidationError('invalid character in name field')
        return value


class ProductSerializer(NestedProductSerializer):
    category = CategorySerializer(read_only=True)

    class Meta(NestedProductSerializer.Meta):
        fields = NestedProductSerializer.Meta.fields + ('category',)

