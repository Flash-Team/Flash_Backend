from django.db import models

# noinspection PyProtectedMember
from flash._auth.models import MyUser
from flash.organization.models import Filial
from flash.product.models import Product


class Order(models.Model):
    address = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)
    client = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='client')
    courier = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='courier')
    delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)


class OrderedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    count = models.IntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
