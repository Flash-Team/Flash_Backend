import logging

from django.http import Http404

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

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
        category_id =product =  self.kwargs.get('parent_lookup_category')
        product = serializer.save(category=Category.objects.get(id=category_id))
  
        LOG.info('Product {} created in {} category for organization {}'.format(product.name, product.category.name,
                                                                                product.organization.name))


@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryDetail(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
