from rest_framework import generics

from flash.organization.models import Organization, Filial
from flash.organization.serializers import OrganizationSerializer, FilialSerializer


class OrganizationsView(generics.ListCreateAPIView):

    def get_queryset(self):
        return Organization.objects.all()

    def get_serializer_class(self):
        return OrganizationSerializer


class OrganizationView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        return Organization.objects.all()

    def get_serializer_class(self):
        return OrganizationSerializer


class FilialsView(generics.ListCreateAPIView):

    def get_queryset(self):
        return Filial.objects.filter(order=self.kwargs.get('pk'))

    def get_serializer_class(self):
        return FilialSerializer

    def perform_create(self, serializer):
        order_id = self.kwargs.get('pk')
        serializer.save(filial=Filial.objects.get(id=order_id))


class FilialView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        return Filial.objects.filter(id=self.kwargs.get('pk'), order=self.kwargs.get('pk2'))

    def get_serializer_class(self):
        return FilialSerializer
