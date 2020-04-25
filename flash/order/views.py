import logging

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from flash.order.filters import DeliveredFilter
from flash.order.models import Order, OrderedProduct
from flash.order.permissions import IsClient
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
        user = self.request.user
        
        if user.is_anonymous:
            return IsAuthenticated(),

        if self.action == 'create':
            if user.is_admin or user.is_client:
                return IsAuthenticated(),

            return IsAdminUser(),

        elif self.action == 'rate':
            if user.is_client:
                return IsClient(),

        elif self.action in ('update', 'partial_update', 'destroy'):
            if user.is_admin or user.is_manager:
                return IsAuthenticated(),

            return IsAdminUser(),

        return IsAuthenticated(),

    def perform_create(self, serializer):
        """
        Set client of order to authorized user
        """
        order = serializer.save(client=self.request.user)

        LOG.info('{} ordered by {}'.format(order, order.client))

    @action(detail=True, methods=['post'], permission_classes=(IsAdminUser,))
    def rate(self, request, pk):
        """
        Rate all products in following order by value (between 0 and 5)
        """
        order = Order.objects.get(id=pk)

        if order.delivered:
            return Response({'message': 'Order already rated'}, status=status.HTTP_400_BAD_REQUEST)

        value = request.query_params.get("value")

        serializer = OrderRateSerializer(self.get_object(), data={'value': value})

        serializer.is_valid(raise_exception=True)
        serializer.save()

        LOG.info('{} delivered and rated for {}'.format(order, value))

        return Response({'message': 'Rated'}, status=status.HTTP_200_OK)


class ProductsViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return OrderedProduct.objects.for_user(self.request.user).filter(order=self.kwargs.get('parent_lookup_order'))

    def get_serializer_class(self):
        return BaseProductSerializer

    def get_permissions(self):
        if self.request.user.is_anonymous:
            return IsAuthenticated(),

        if self.request.method in ('PUT', 'PATCH', 'DELETE', 'POST'):
            if self.request.user.role in (1, 2):
                return IsAuthenticated(),

            return IsAdminUser(),

        return IsAuthenticated(),

    def perform_create(self, serializer):
        """
        Use id of order in url
        """
        order_id = self.kwargs.get('parent_lookup_order')
        order = Order.objects.get(id=order_id)
        serializer.save(order=order)
