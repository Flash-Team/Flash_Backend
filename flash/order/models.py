from django.db import models
from django.utils import timezone
from flash._auth.models import MyUser
from flash.product.models import Product
from django.core.validators import MinValueValidator


class Order(models.Model):
    address = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # filial = models.ForeignKey(None, on_delete=models.CASCADE)
    client = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='client')
    courier = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='courier')
    delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

class OrderedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1, validators=[MinValueValidator])
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
