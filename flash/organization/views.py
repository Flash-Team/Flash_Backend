from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from flash.organization.models import Organization, Filial
from flash.organization.serializers import OrganizationSerializer, FilialSerializer, OrganizationRateSerializer, \
    NestedFilialSerializer


class OrganizationsViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Organization.objects.for_user(self.request.user)

    def get_serializer_class(self):
        return OrganizationSerializer

    def get_permissions(self):
        if self.request.user.is_anonymous:
            return IsAuthenticated(),

        if self.request.method in ('PUT', 'PATCH', 'DELETE', 'POST'):
            if self.request.user.role in (1, 2):
                return IsAuthenticated(),

            return IsAdminUser(),

        return IsAuthenticated(),

    def perform_create(self, serializer):
        organization = serializer.save(manager=self.request.user)

    @action(detail=True, methods=['patch'], )
    def rate(self, request, pk):
        value = request.query_params.get('value')

        serializer = OrganizationRateSerializer(self.get_object(), data={'value': value})

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'rated'}, status=status.HTTP_200_OK)


class FilialsViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Filial.objects.filter(organization=self.kwargs.get('parent_lookup_organization'))

    def get_serializer_class(self):
        if self.request.method in ('POST', 'GET'):
            return FilialSerializer

        return NestedFilialSerializer

    def get_permissions(self):
        if self.request.user.is_anonymous:
            return IsAuthenticated(),

        if self.request.method in ('PUT', 'PATCH', 'DELETE', 'POST'):
            if self.request.user.role in (1, 2):
                return IsAuthenticated(),

            return IsAdminUser(),

        return IsAuthenticated(),

    def perform_create(self, serializer):
        organization_id = self.kwargs.get('parent_lookup_organization')
        serializer.save(organization=Organization.objects.get(id=organization_id))
