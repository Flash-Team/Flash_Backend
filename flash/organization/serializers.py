from rest_framework import serializers

from flash.organization.models import Organization, Filial


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'description', 'logo',)


class FilialSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    class Meta:
        model = Filial
        fields = ('id', 'address', 'organization',)
