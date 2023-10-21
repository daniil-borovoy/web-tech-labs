from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.forms import model_to_dict

from labs.models import Supply, Log, Supplier, Product, Sale


@receiver([pre_save, pre_delete], sender=Supplier)
@receiver([pre_save, pre_delete], sender=Product)
@receiver([pre_save, pre_delete], sender=Sale)
@receiver([pre_save, pre_delete], sender=Supply)
def log(sender, instance, **kwargs):
    save_log(instance)


@receiver(pre_save, sender=Sale)
@receiver(pre_save, sender=Supply)
def post_save_sale_or_supply(sender, instance, **kwargs):
    if isinstance(instance, Supply):
        product = Product.objects.filter(id=instance.product.id).first()
        old_supply = Supply.objects.filter(id=instance.id).first()
        if not old_supply:
            new_count = product.count + instance.count
            product.count = new_count
            product.save()
        else:
            new_count = (product.count - old_supply.count) + instance.count
            product.count = new_count
            product.save()

    elif isinstance(instance, Sale):
        product = Product.objects.filter(id=instance.product.id).first()
        old_sale = Sale.objects.filter(id=instance.id).first()

        if not old_sale:
            new_count = product.count - instance.count
            product.count = new_count
            product.save()
        else:
            new_count = (product.count + old_sale.count) - instance.count
            product.count = new_count
            product.save()


def save_log(instance):
    if not instance.id:
        return

    old_value = instance.__class__.objects.get(id=instance.id)
    Log.objects.create(data=model_to_dict(old_value))
