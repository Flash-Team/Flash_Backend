from rest_framework import generics

from flash.order.models import Order, OrderedProduct
from flash.order.serializers import OrderSerializer, ProductSerializer


class OrdersView(generics.ListCreateAPIView):

    def get_queryset(self):
        return Order.objects.all()

    def get_serializer_class(self):
        return OrderSerializer


class OrderView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        return Order.objects.all()

    def get_serializer_class(self):
        return OrderSerializer


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
