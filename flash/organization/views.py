from rest_framework import viewsets

from flash.organization.models import Organization, Filial
from flash.organization.serializers import OrganizationSerializer, FilialSerializer


class OrganizationsViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Organization.objects.all()

    def get_serializer_class(self):
        return OrganizationSerializer


class FilialsViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Filial.objects.filter(organization=self.kwargs.get('parent_lookup_organization'))

    def get_serializer_class(self):
        return FilialSerializer

    def perform_create(self, serializer):
        organization_id = self.kwargs.get('parent_lookup_organization')
        serializer.save(organization=Organization.objects.get(id=organization_id))
