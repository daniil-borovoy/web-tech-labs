from django.urls import path, include

from . import views
from .query_urls import queries
from .views import Lab2TablePageView

urlpatterns = [
    path("tables/<str:table_name>/", Lab2TablePageView.as_view(), name="table"),
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
    path("queries/", include(queries)),
]
