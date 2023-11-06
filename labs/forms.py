from django import forms
from django.contrib.auth.models import User

from .models import Supplier, Sale, Supply, Product, Log


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


class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = "__all__"


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        exclude = ["password", "last_login"]


table_name_to_form_map = {
    Supplier.__name__: SupplierForm,
    Sale.__name__: SaleForm,
    Supply.__name__: SupplyForm,
    Product.__name__: ProductForm,
    Log.__name__: LogForm,
    User.__name__: UserForm,
}

table_model_name_to_form_map = {
    Supplier._meta.model_name: SupplierForm,
    Sale._meta.model_name: SaleForm,
    Supply._meta.model_name: SupplyForm,
    Product._meta.model_name: ProductForm,
    Log._meta.model_name: LogForm,
    User._meta.model_name: UserForm,
}
