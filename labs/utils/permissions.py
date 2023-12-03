from functools import lru_cache

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from labs.models import Log, Product, Supply, Supplier, Sale


@lru_cache
def get_admin_module_permissions():
    content_types = [
        ContentType.objects.get_for_model(Log),
        ContentType.objects.get_for_model(Product),
        ContentType.objects.get_for_model(Supply),
        ContentType.objects.get_for_model(Supplier),
        ContentType.objects.get_for_model(Sale),
    ]

    permissions = Permission.objects.filter(content_type__in=content_types)

    permissions = ["labs." + perm.codename for perm in permissions]

    return permissions
