from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

from flash.organization.models import Organization, Filial
from flash.organization.serializers import OrganizationSerializer, FilialSerializer, OrganizationRateSerializer


class OrganizationsViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Organization.objects.all()

    def get_serializer_class(self):
        return OrganizationSerializer

    @action(detail=True, methods=['patch'])
    def rate(self, request, pk):
        value = int(self.request.query_params.get('value'))

        serializer = OrganizationRateSerializer(self.get_object(), data={'value': value})

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'rated'}, status=status.HTTP_200_OK)


class FilialsViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Filial.objects.filter(organization=self.kwargs.get('parent_lookup_organization'))

    def get_serializer_class(self):
        return FilialSerializer

    def perform_create(self, serializer):
        organization_id = self.kwargs.get('parent_lookup_organization')
        serializer.save(organization=Organization.objects.get(id=organization_id))
