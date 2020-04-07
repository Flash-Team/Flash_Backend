from django.db import models

# noinspection PyProtectedMember
from flash._auth.models import MyUser
from flash.organization.models import Organization
from flash.product.bases import BaseProduct


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Categories'


class Product(BaseProduct):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
