from django.db import models

# noinspection PyProtectedMember
from flash._auth.models import MyUser
from flash.organization.validators import validate_file_size, validate_extension
from flash.product.bases import BaseProduct


class Organization(BaseProduct):
    logo = models.FileField(upload_to='organizations_logo', null=True, blank=True, validators=[validate_file_size,
                                                                                               validate_extension, ])
    manager = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='organizations')

    def rate(self, value):
        self.sum += value
        self.count += 1
        self.save()

    def __str__(self):
        return self.name


class Filial(models.Model):
    address = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organizations')

    def __str__(self):
        return '{} [address: {}, organization: {}]'.format('Filial', self.address, self.organization)
