from django.urls import path

from . import views
from .views import Lab3TableView

urlpatterns = [
    path("tables/<str:table_name>/", Lab3TableView.as_view(), name="table"),
    path("tables/<str:table_name>/add", views.entity_page, name="add_entity"),
    path(
        "tables/<str:table_name>/<int:entity_id>/change",
        views.entity_page,
        name="edit_entity",
    ),
    path(
        "tables/<str:table_name>/delete/<int:entity_id>",
        views.delete_entity,
        name="delete_entity",
    ),
]
