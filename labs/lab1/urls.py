from django.urls import path

from labs.lab1.views import ProductFormView, SupplierFormView

urlpatterns = [
    path("product-form/", ProductFormView.as_view()),
    path("supplier-form/", SupplierFormView.as_view()),
]
