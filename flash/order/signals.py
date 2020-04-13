from django.db.models.signals import post_save
from django.dispatch import receiver

# noinspection PyProtectedMember
from flash._auth.models import MyUser
from flash.order.models import Order


@receiver(post_save, sender=Order)
def find_courier(sender, instance, created, **kwargs):
    """
    For created order find courier that have less undone orders
    """
    if created:
        courier = None

        for user in MyUser.objects.all():
            # 4 - Courier role id
            if user.role == 4:

                if not courier:
                    courier = user

                if user.undone_orders.count() < courier.undone_orders.count():
                    courier = user

        instance.set_courier(courier)
