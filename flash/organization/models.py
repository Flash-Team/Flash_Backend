from django.db import models

# noinspection PyProtectedMember
from flash._auth.models import MyUser
from flash.product.models import QWE


class Organization(QWE):
    manager = models.ForeignKey(MyUser, on_delete=models.CASCADE)


class Filial(models.Model):
    address = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)