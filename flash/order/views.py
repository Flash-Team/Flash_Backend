from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from flash.order.filters import OrderFilter
from flash.order.models import Order, OrderedProduct
from flash.order.serializers import OrderSerializer, ProductSerializer, OrderRateSerializer, OrderProductsSerializer


class OrdersViewSet(viewsets.ModelViewSet):

    filter_backends = [OrderFilter, ]

    def get_queryset(self):
        return Order.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderProductsSerializer

        return OrderSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            if self.request.user.role in (1, 3):
                return IsAuthenticated(),

            return IsAdminUser(),

        return IsAuthenticated(),

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    @action(detail=True, methods=['patch'])
    def rate(self, request, pk):
        """
        Rate all products in following order by value (between 0 and 5)
        """
        value = int(self.request.query_params.get('value'))

        serializer = OrderRateSerializer(self.get_object(), data={'value': value})

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'rated'}, status=status.HTTP_200_OK)


class ProductsViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return OrderedProduct.objects.filter(order=self.kwargs.get('parent_lookup_order'))

    def get_serializer_class(self):
        return ProductSerializer

    def perform_create(self, serializer):
        order_id = self.kwargs.get('parent_lookup_order')
        serializer.save(order=Order.objects.get(id=order_id))
