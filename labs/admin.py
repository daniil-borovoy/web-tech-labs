from django.contrib import admin

from labs.models import Product, Sale, Supply, Supplier, Log


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    pass


@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    pass


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    pass


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    pass
