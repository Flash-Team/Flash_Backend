from django.db import models

# noinspection PyProtectedMember
from flash._auth.models import MyUser
from flash.product.bases import BaseProduct


class Organization(BaseProduct):
    manager = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def rate(self, value):
        self.sum += value
        self.count += 1


class Filial(models.Model):
    address = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organizations')
