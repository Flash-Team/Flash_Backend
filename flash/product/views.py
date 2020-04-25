from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from flash.product.models import Category, Product
from flash.product.serializers import CategorySerializer, ProductSerializer, NestedProductSerializer


class CategoriesViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Category.objects.all()

    def get_serializer_class(self):
        return CategorySerializer


class ProductsListViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Product.objects.filter(category=self.kwargs.get('parent_lookup_category'))

    def get_serializer_class(self):
        if self.request.method in ('POST', 'GET'):
            return ProductSerializer

        return NestedProductSerializer

    def perform_create(self, serializer):
        category_id = self.kwargs.get('parent_lookup_category')
        serializer.save(category=Category.objects.get(id=category_id))
