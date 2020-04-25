import os

from django.db import models

# noinspection PyProtectedMember
from flash._auth.models import MyUser
from flash.organization.models import Organization
from flash.product.bases import BaseProduct
from flash.product.validators import validate_file_size, validate_extension


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(BaseProduct):
    logo = models.FileField(upload_to='products_logo', null=True, blank=True, validators=[validate_file_size,
                                                                                          validate_extension, ])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return '{} [name: {}, price: {}]'.format('Product', self.name, self.price)
