import enum

from django.contrib.auth.models import Group


class GroupName(enum.Enum):
    admin = "Admins"
    manager = "Managers"
    user = "Users"
    guest = "Guests"


class AdminGroup(Group):
    name = GroupName.admin


class ManagerGroup(Group):
    name = GroupName.manager


class UserGroup(Group):
    name = GroupName.user


class GuestGroup(Group):
    name = GroupName.guest
