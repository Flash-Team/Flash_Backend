from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from flash.order.models import Order, OrderedProduct
from flash.order.serializers import OrderSerializer, ProductSerializer, OrderRateSerializer


class OrdersViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Order.objects.all()

    def get_serializer_class(self):
        return OrderSerializer

    @action(detail=True, methods=['patch'])
    def rate(self, request, pk):
        value = int(self.request.query_params.get('value'))

        serializer = OrderRateSerializer(self.get_object(), value=value)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'rated'}, status=status.HTTP_200_OK)


class ProductsView(generics.ListCreateAPIView):

    def get_queryset(self):
        return OrderedProduct.objects.filter(order=self.kwargs.get('pk'))

    def get_serializer_class(self):
        return ProductSerializer

    def perform_create(self, serializer):
        order_id = self.kwargs.get('pk')
        serializer.save(order=Order.objects.get(id=order_id))


class ProductView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        return OrderedProduct.objects.filter(id=self.kwargs.get('pk'), order=self.kwargs.get('pk2'))

    def get_serializer_class(self):
        return ProductSerializer
