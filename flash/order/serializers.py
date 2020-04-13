from rest_framework import serializers

# noinspection PyProtectedMember
from flash._auth.serializers import CourierSerializer, ClientSerializer
from flash.order.models import Order, OrderedProduct
from flash.order.validators import positive_number_validator, rating_validator


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'filial', 'address', 'client', 'courier', 'delivered', 'price',)


class NestedProductSerializer(serializers.ModelSerializer):

    count = serializers.IntegerField(validators=[positive_number_validator])

    class Meta:
        model = OrderedProduct
        fields = ('id', 'product', 'count',)


class ProductSerializer(NestedProductSerializer):

    order = OrderSerializer(read_only=True)

    class Meta(NestedProductSerializer.Meta):
        fields = NestedProductSerializer.Meta.fields + ('order',)


class OrderRateSerializer(serializers.Serializer):

    value = serializers.IntegerField(validators=[rating_validator])

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):

        for product in instance.products.all():
            product.product.sum += validated_data.get('value')
            product.product.count += 1

            product.product.save()

        instance.complete()

        return instance


class OrderProductsSerializer(serializers.ModelSerializer):

    products = NestedProductSerializer(many=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    courier = CourierSerializer(read_only=True)
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'filial', 'address', 'client', 'price', 'delivered', 'products', 'courier',)

    def create(self, validated_data):
        products = validated_data.pop('products')

        return Order.create(validated_data, products)
