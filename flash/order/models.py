from django.db import models

# noinspection PyProtectedMember
from flash._auth.models import MyUser
from flash.organization.models import Filial
from flash.product.models import Product


# Filter orders for all roles of user
class OrderManager(models.Manager):

    def for_user(self, user):
        if user.role == 1:
            return self.all()

        # Todo: check it!
        elif user.role == 2:
            return self.filter(filial__organization__manager=user)

        elif user.role == 3:
            return self.filter(client=user)

        elif user.role == 4:
            return self.filter(courier=user)

        return self.all()


class Order(models.Model):

    address = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, related_name='orders')
    client = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='ordered')
    courier = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='orders', null=True, default=None)
    delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    objects = OrderManager()

    def save_price(self, value):
        self.price = value
        self.save()

    def set_courier(self, courier):
        self.courier = courier
        self.save()

    def complete(self):
        self.delivered = True
        self.save()

    def calculate_price(self):
        price = 0

        for product in self.products.all():
            price += product.price

        self.price = price

        self.save()

    def rate(self, value):
        for product in self.products.all():
            product.product.sum += value
            product.product.count += 1

            product.product.save()

    @classmethod
    def create(cls, order_data, products):
        order = Order.objects.create(**order_data)

        order.save()

        price = 0

        for pr in products:
            product = OrderedProduct.objects.create(**pr, order=order)

            product.save()

            price += product.price

        order.save_price(price)

        return order

    def __str__(self):
        return '{} [price: {}, address: {}]'.format('Order', self.price, self.address)


class OrderedProduct(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    count = models.IntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')

    @property
    def price(self):
        return self.product.price * self.count

    def __str__(self):
        return '{} [count: {}]'.format(self.product, self.count)
