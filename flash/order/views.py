import logging

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from flash.order.filters import DeliveredFilter
from flash.order.models import Order, OrderedProduct
from flash.order.serializers import BaseOrderSerializer, OrderRateSerializer, OrderProductsSerializer, \
    BaseProductSerializer

LOG = logging.getLogger('info')


class OrdersViewSet(viewsets.ModelViewSet):

    filter_backends = [DeliveredFilter, ]

    def get_queryset(self):
        return Order.objects.for_user(self.request.user)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'GET'):
            return OrderProductsSerializer

        return BaseOrderSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            if self.request.user.role in (1, 3):
                return IsAuthenticated(),

            return IsAdminUser(),

        elif self.request.method in ('PUT', 'PATCH', 'DELETE'):
            if self.request.user.role in (1, 2):
                return IsAuthenticated(),

            return IsAdminUser(),

        return IsAuthenticated(),

    def perform_create(self, serializer):
        order = serializer.save(client=self.request.user)

        LOG.info('{} ordered by {}'.format(order, order.client))

    @action(detail=True, methods=['post'])
    def rate(self, request, pk):
        """
        Rate all products in following order by value (between 0 and 5)
        """
        order = Order.objects.get(id=pk)

        if order.delivered:
            return Response({'message': 'Order already rated'}, status=status.HTTP_400_BAD_REQUEST)

        value = int(self.request.query_params.get('value'))

        serializer = OrderRateSerializer(self.get_object(), data={'value': value})

        serializer.is_valid(raise_exception=True)
        serializer.save()

        LOG.info('{} delivered and rated for {}'.format(order, value))

        return Response({'message': 'Rated'}, status=status.HTTP_200_OK)


class ProductsViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return OrderedProduct.objects.filter(order=self.kwargs.get('parent_lookup_order'))

    def get_serializer_class(self):
        return BaseProductSerializer

    def perform_create(self, serializer):
        order_id = self.kwargs.get('parent_lookup_order')
        order = Order.objects.get(id=order_id)
        serializer.save(order=order)

        order.calculate_price()

    def perform_update(self, serializer):
        order_id = self.kwargs.get('parent_lookup_order')
        order = Order.objects.get(id=order_id)
        serializer.save(id=order_id)

        order.calculate_price()

    def perform_destroy(self, instance):
        order_id = self.kwargs.get('parent_lookup_order')
        order = Order.objects.get(id=order_id)
        instance.delete()

        order.calculate_price()
