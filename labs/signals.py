from django.db.models.signals import post_delete, post_save, pre_save, pre_delete
from django.dispatch import receiver
from django.forms import model_to_dict

from labs.models import Supply, Log, Supplier, Product, Sale


def save_log(instance):
    if instance.id:
        old_value = instance.__class__.objects.get(id=instance.id)
        Log.objects.create(data=model_to_dict(old_value))


@receiver(pre_delete, sender=Supply)
@receiver(pre_save, sender=Supply)
def log_supply(sender, instance, **kwargs):
    save_log(instance)


@receiver(pre_delete, sender=Supplier)
@receiver(pre_save, sender=Supplier)
def log_supply(sender, instance, **kwargs):
    save_log(instance)


@receiver(pre_delete, sender=Product)
@receiver(pre_save, sender=Product)
def log_supply(sender, instance, **kwargs):
    save_log(instance)


@receiver(pre_delete, sender=Sale)
@receiver(pre_save, sender=Sale)
def log_sale(sender, instance, **kwargs):
    save_log(instance)
