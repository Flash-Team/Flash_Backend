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


# Ensure that value of rating is between 0 and 5
def rating_validator(value):
    if value > 5 or value <= 0:
        raise serializers.ValidationError('Invalid rating value')


class OrderRateSerializer(serializers.Serializer):

    value = serializers.IntegerField(validators=[rating_validator])

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):

        for product in instance.products.all():
            product.product.sum += validated_data.get('value')
            product.product.count += 1

            product.product.save()

        return instance
