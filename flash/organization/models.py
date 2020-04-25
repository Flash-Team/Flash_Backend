from django.db import models

# noinspection PyProtectedMember
from flash._auth.models import MyUser
from flash.product.bases import BaseProduct


class OrganizationManager(models.Manager):

    def for_user(self, user):
        return self.filter(manager=user)


class Organization(BaseProduct):
    manager = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    objects = OrganizationManager()

    def rate(self, value):
        self.sum += value
        self.count += 1
        self.save()

    def __str__(self):
        return '{} [name: {}, logo: {}]'.format('Organization', self.name, self.logo)


class Filial(models.Model):
    address = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organizations')

    def __str__(self):
        return '{} [address: {}, organization: {}]'.format('Filial', self.address, self.organization)
