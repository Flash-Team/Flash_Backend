import os

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from flash.organization.models import Organization, Filial


@receiver(post_save, sender=Organization)
def organization_created(sender, instance, created, **kwargs):

    """
    Creates filial with empty information,
    when Organization object is created
    """

    if created:
        Filial.objects.create(name='Filials of organization', organization=instance)


@receiver(post_delete, sender=Organization)
def auto_delete_logo_on_delete(sender, instance, **kwargs):
    """
    Deletes logo from filesystem
    when Organization object is deleted.
    """
    if instance.logo:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)


@receiver(pre_save, sender=Organization)
def auto_delete_logo_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when Organization object is updated
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
