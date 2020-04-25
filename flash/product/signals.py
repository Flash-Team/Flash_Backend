import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from flash.product.models import Product


@receiver(post_delete, sender=Product)
def auto_delete_logo_on_delete(sender, instance, **kwargs):
    """
    Deletes logo from filesystem
    when Product object is deleted.
    """
    if instance.logo:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)


@receiver(pre_save, sender=Product)
def auto_delete_logo_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when Product object is updated
    with a new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).logo
    except sender.DoesNotExist:
        return False

    new_file = instance.logo
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
