from labs.models import Supplier, Sale, Supply, Product

table_name_to_table_map = {
    Supplier.__name__: Supplier,
    Sale.__name__: Sale,
    Supply.__name__: Supply,
    Product.__name__: Product,
}

tables = [
    {"name": "Поставщики", "link": Supplier.__name__},
    {"name": "Продажи", "link": Sale.__name__},
    {"name": "Поставки", "link": Supply.__name__},
    {"name": "Товары", "link": Product.__name__},
]
