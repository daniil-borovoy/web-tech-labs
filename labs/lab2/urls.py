from django.urls import path, include

from . import views
from .query_urls import queries
from .views import Lab2TablePageView

urlpatterns = [
    path("tables/<str:slug>/", Lab2TablePageView.as_view(), name="table"),
    path("tables/<str:slug>/add", views.entity_page, name="add_entity"),
    path(
        "tables/<str:slug>/<int:entity_id>/change",
        views.entity_page,
        name="edit_entity",
    ),
    path(
        "tables/<str:slug>/delete/<int:entity_id>",
        views.delete_entity,
        name="delete_entity",
    ),
    path("queries/", include(queries)),
]
