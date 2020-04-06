from rest_framework import generics

from flash.product.models import Category, Product
from flash.product.serializers import CategorySerializer, Product2Serializer


class CategoriesView(generics.ListCreateAPIView):

    def get_queryset(self):
        return Category.objects.all()

    def get_serializer_class(self):
        return CategorySerializer


class CategoryView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        return Category.objects.all()

    def get_serializer_class(self):
        return CategorySerializer


class ProductsListView(generics.ListCreateAPIView):

    def get_queryset(self):
        return Product.objects.filter(order=self.kwargs.get('pk'))

    def get_serializer_class(self):
        return Product2Serializer

    def perform_create(self, serializer):
        order_id = self.kwargs.get('pk')
        serializer.save(category=Category.objects.get(id=order_id))


class ProductListView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        return Product.objects.filter(id=self.kwargs.get('pk'), order=self.kwargs.get('pk2'))

    def get_serializer_class(self):
        return Product2Serializer
