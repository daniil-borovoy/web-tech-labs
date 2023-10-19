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


class Supplier(Model):
    name = CharField(max_length=255)
    address = CharField(max_length=255)
    phone = CharField(max_length=255)
    who_to_contact = CharField(max_length=255, db_column="")
    deleted = BooleanField(default=False)

    class Meta:
        db_table = "suppliers"

    def __str__(self):
        return self.name


class Product(Model):
    name = CharField(max_length=255)
    price = FloatField()
    receipt_date = DateField(default=datetime.date.today)
    count = IntegerField()
    deleted = BooleanField(default=False)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.name


class Supply(Model):
    supplier = ForeignKey(Supplier, on_delete=CASCADE, db_column="supplier_id")
    product = ForeignKey(Product, on_delete=CASCADE, db_column="product_id")
    count = IntegerField(default=0)
    deleted = BooleanField(default=False)

    class Meta:
        db_table = "supplies"

    def __str__(self):
        return f"{self.supplier.name} - {self.product.name}"


class Sale(Model):
    product = ForeignKey(Product, on_delete=CASCADE, db_column="product_id")
    date = DateField()
    count = IntegerField()
    retail_price = FloatField()
    deleted = BooleanField(default=False)

    class Meta:
        db_table = "sales"

    def __str__(self):
        return f"Sale - {self.id}"


class Log(Model):
    data = JSONField(encoder=DjangoJSONEncoder)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = "logs"

    def __str__(self):
        return f"Log - {self.id}"
