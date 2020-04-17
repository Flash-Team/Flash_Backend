from rest_framework import serializers

# noinspection PyProtectedMember
from flash._auth.serializers import CourierSerializer, ClientSerializer
from flash.order.models import Order, OrderedProduct
from flash.order.validators import positive_number_validator, rating_validator


class BaseOrderSerializer(serializers.ModelSerializer):

    courier = CourierSerializer(read_only=True)
    client = ClientSerializer(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'filial', 'address', 'client', 'price', 'delivered', 'courier',)


class BaseProductSerializer(serializers.ModelSerializer):

    count = serializers.IntegerField(validators=[positive_number_validator])

    class Meta:
        model = OrderedProduct
        fields = ('id', 'product', 'count',)


class OrderProductsSerializer(BaseOrderSerializer):

    products = BaseProductSerializer(many=True)

    class Meta(BaseOrderSerializer.Meta):
        fields = BaseOrderSerializer.Meta.fields + ('products',)

    def create(self, validated_data):
        """
        Create order with ordered products together
        """
        products = validated_data.pop('products')

        return Order.create(validated_data, products)


class ProductSerializer(BaseProductSerializer):

    order = BaseOrderSerializer(read_only=True)

    class Meta(BaseProductSerializer.Meta):
        fields = BaseProductSerializer.Meta.fields + ('order',)


class OrderRateSerializer(serializers.Serializer):
    """
    Serializer for rating products in order for rating value
    """

    value = serializers.IntegerField(validators=[rating_validator])

    def create(self, validated_data):
        """
        Cannot create order here
        """
        pass

    def update(self, instance, validated_data):
        """
        Update each product in order, add value of rating and increase number of rates by 1
        """
        instance.rate(validated_data.get('value'))

        instance.complete()

        return instance
