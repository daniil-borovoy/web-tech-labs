from django.db.models import (
    Model,
    CharField,
    BooleanField,
    FloatField,
    DateField,
    IntegerField,
    ForeignKey,
    CASCADE
)


class Supplier(Model):
    name = CharField(max_length=50)
    address = CharField(max_length=50)
    phone = CharField(max_length=50)
    who_to_contact = CharField(max_length=50)
    deleted = BooleanField(default=False)

    class Meta:
        db_table = "suppliers"

    def __str__(self):
        return self.name


class Product(Model):
    name = CharField(max_length=50)
    price = FloatField()
    receipt_date = DateField()
    count = IntegerField()
    deleted = BooleanField(default=False)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.name


class Supply(Model):
    supplier = ForeignKey(Supplier, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)
    deleted = BooleanField(default=False)

    class Meta:
        db_table = "supplies"

    def __str__(self):
        return f"{self.supplier.name} - {self.product.name}"


class Sale(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    date = DateField()
    count = IntegerField()
    retail_price = FloatField()
    deleted = BooleanField(default=False)

    class Meta:
        db_table = "sales"

    def __str__(self):
        return f"Sale - {self.id}"
