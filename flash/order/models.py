from django.db import models

# noinspection PyProtectedMember
from flash._auth.models import MyUser
from flash.organization.models import Filial
from flash.product.models import Product


class Order(models.Model):
    address = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)
    client = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='ordered')
    courier = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='orders', null=True, default=None)
    delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def set_price(self, value):
        self.price = value
        self.save()

    def set_courier(self, courier):
        self.courier = courier
        self.save()

    def complete(self):
        self.delivered = True
        self.save()

    @classmethod
    def create(cls, order_data, products):
        order = Order.objects.create(**order_data)

        order.save()

        price = 0

        for pr in products:
            product = OrderedProduct.objects.create(**pr, order=order)

            product.save()

            price += product.price

        order.set_price(price)

        return order


class OrderedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    count = models.IntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')

    @property
    def price(self):
        return self.product.price * self.count
