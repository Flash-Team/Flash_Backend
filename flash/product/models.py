from django.db import models

# noinspection PyProtectedMember
from flash._auth.models import MyUser
from flash.organization.models import Organization


# Abstract class, base for Product and Organization (in future)
# Need to find appropriate name
class QWE(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    logo = models.CharField(max_length=999)                         # indeed url field
    rating = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Categories'


class Product(QWE):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
