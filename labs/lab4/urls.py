from django.contrib.auth.views import LogoutView
from django.urls import path, include

from .views import (
    SignUpView,
    SignInView,
    AdminModuleView,
    AdminTableView,
    # AdminEntityView,
)
from ..utils.entity_view import (
    create_edit_view,
    create_add_view,
    create_delete_view,
)

auth_urls = [
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
    path("sign-in/", SignInView.as_view(), name="sign-in"),
    path("sign-out/", LogoutView.as_view(next_page="/auth/sign-in")),
]

admin_module_urls = [
    path("", AdminModuleView.as_view()),
    path("<str:table_name>/<int:page>", AdminTableView.as_view(), name="admin-table"),
    path("<str:table_name>/add", create_add_view, name="admin-add"),
    path(
        "<str:table_name>/<int:entity_id>/change/",
        create_edit_view,
        name="admin-change",
    ),
    path(
        "<str:table_name>/<pk>/delete/",
        create_delete_view,
        name="admin-delete",
    ),
]

urlpatterns = [
    path("auth/", include(auth_urls)),
    path("admin-module/", include(admin_module_urls)),
]
