import datetime

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import (
    Model,
    CharField,
    BooleanField,
    FloatField,
    DateField,
    IntegerField,
    ForeignKey,
    CASCADE,
    JSONField,
    DateTimeField,
)
from django.utils.translation import gettext as _


class Supplier(Model):
    name = CharField(max_length=255, verbose_name=_("Name"))
    address = CharField(max_length=255, verbose_name=_("Address"))
    phone = CharField(max_length=255, verbose_name=_("Phone"))
    # TODO: db_column?
    who_to_contact = CharField(max_length=255, db_column="", verbose_name=_("Who to contact"))
    deleted = BooleanField(default=False, verbose_name=_("Deleted"))

    class Meta:
        db_table = "suppliers"
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")

    def __str__(self):
        return self.name


class Product(Model):
    name = CharField(max_length=255, verbose_name=_("Name"))
    price = FloatField(verbose_name=_("Price"))
    receipt_date = DateField(default=datetime.date.today, verbose_name=_("Receipt date"))
    count = IntegerField(verbose_name=_("Count"))
    deleted = BooleanField(default=False, verbose_name=_("Deleted"))

    class Meta:
        db_table = "products"
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name


class Supply(Model):
    supplier = ForeignKey(Supplier, on_delete=CASCADE, db_column="supplier_id", verbose_name=_("Supplier"))
    product = ForeignKey(Product, on_delete=CASCADE, db_column="product_id", verbose_name=_("Product"))
    count = IntegerField(default=0, verbose_name=_("Count"))
    created_at = DateTimeField(auto_created=True, editable=False, verbose_name=_("Created at"))
    deleted = BooleanField(default=False, verbose_name=_("Deleted"))

    class Meta:
        db_table = "supplies"
        verbose_name = _("Supply")
        verbose_name_plural = _("Supplies")

    def __str__(self):
        return f"{self.supplier.name} - {self.product.name}"


class Sale(Model):
    product = ForeignKey(Product, on_delete=CASCADE, db_column="product_id", verbose_name=_("Product"))
    date = DateField(verbose_name=_("Date"))
    count = IntegerField(verbose_name=_("Count"))
    retail_price = FloatField(verbose_name=_("Retail price"))
    deleted = BooleanField(default=False, verbose_name=_("Deleted"))

    class Meta:
        db_table = "sales"
        verbose_name = _("Sale")
        verbose_name_plural = _("Sales")

    def __str__(self):
        return f"{_("Sale")} - {self.id}"


class Log(Model):
    data = JSONField(encoder=DjangoJSONEncoder, verbose_name=_("Data"))
    created_at = DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        db_table = "logs"
        verbose_name = _("Log")
        verbose_name_plural = _("Logs")

    def __str__(self):
        return f"{_("Log")} - {self.id}"
