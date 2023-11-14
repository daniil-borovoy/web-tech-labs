from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group

# Create groups
admin_group, created = Group.objects.get_or_create(name="Admins")


def in_admin_group(user):
    if user and user.is_authenticated:
        return user.groups.filter(name=admin_group.name).exists()
    return False


in_admin_group_required = user_passes_test(in_admin_group)
