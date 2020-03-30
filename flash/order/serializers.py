from rest_framework import serializers

from flash.order.models import Order, OrderedProduct


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'filial', 'address', 'client', 'courier', 'delivered', 'price',)


# Ensure that count of product is positive
def positive_number_validator(value):
    if value < 0:
        raise serializers.ValidationError('Count must be positive')


class ProductSerializer(serializers.ModelSerializer):

    count = serializers.IntegerField(validators=[positive_number_validator])
    order = OrderSerializer(read_only=True)

    class Meta:
        model = OrderedProduct
        fields = ('id', 'product', 'count', 'order',)
