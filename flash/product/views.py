import logging

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from flash.product.models import Category, Product
from flash.product.serializers import CategorySerializer, ProductSerializer, NestedProductSerializer

LOG = logging.getLogger('info')


class CategoriesViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Category.objects.all()

    def get_permissions(self):
        if self.request.user.is_anonymous:
            return IsAuthenticated(),

        if self.request.method in ('PUT', 'PATCH', 'DELETE', 'POST'):
            if self.request.user.role in (1, 2):
                return IsAuthenticated(),

            return IsAdminUser(),

        return IsAuthenticated(),

    def get_serializer_class(self):
        return CategorySerializer

    def perform_create(self, serializer):
        category = serializer.save()

        LOG.info('Category {} created'.format(category.name))


class ProductsListViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Product.objects.filter(category=self.kwargs.get('parent_lookup_category'))

    def get_permissions(self):
        if self.request.user.is_anonymous:
            return IsAuthenticated(),

        if self.request.method in ('PUT', 'PATCH', 'DELETE', 'POST'):
            if self.request.user.role in (1, 2):
                return IsAuthenticated(),

            return IsAdminUser(),

        return IsAuthenticated(),

    def get_serializer_class(self):
        if self.request.method in ('POST', 'GET'):
            return ProductSerializer

        return NestedProductSerializer

    def perform_create(self, serializer):
        category_id = self.kwargs.get('parent_lookup_category')
        product = serializer.save(category=Category.objects.get(id=category_id))

        LOG.info('Product {} created in {} category for organization {}'.format(product.name, product.category.name,
                                                                                product.organization.name))
