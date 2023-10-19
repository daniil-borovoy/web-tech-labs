from django import forms
from django.forms import IntegerField, CharField

from .models import Supplier, Sale, Supply, Product


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"
        exclude = ["deleted"]


class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = "__all__"
        exclude = ["deleted"]


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = "__all__"
        exclude = ["deleted"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ["deleted"]


table_name_to_form_map = {
    Supplier.__name__: SupplierForm,
    Sale.__name__: SaleForm,
    Supply.__name__: SupplyForm,
    Product.__name__: ProductForm,
}
