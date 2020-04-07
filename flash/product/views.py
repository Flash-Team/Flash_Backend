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
        return Product.objects.filter(category=self.kwargs.get('pk'))

    def get_serializer_class(self):
        return Product2Serializer

    def perform_create(self, serializer):
        category_id = self.kwargs.get('pk')
        serializer.save(category=Category.objects.get(id=category_id))


class ProductListView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        return Product.objects.filter(id=self.kwargs.get('pk'), category=self.kwargs.get('pk2'))

    def get_serializer_class(self):
        return Product2Serializer
