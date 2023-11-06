from labs.models import Supplier, Sale, Supply, Product

menu_tables = [
    {"name": "Поставщики", "link": f"tables/{Supplier.__name__}"},
    {"name": "Продажи", "link": f"tables/{Sale.__name__}"},
    {"name": "Поставки", "link": f"tables/{Supply.__name__}"},
    {"name": "Товары", "link": f"tables/{Product.__name__}"},
]

menu_queries = [
    {
        "name": "Перечень поставщиков, расположенных по адресу в г. Москва",
        "link": "queries/suppliers-in-city",
    },
    {
        "name": "Cписок товаров, проданных за сегодняшний день",
        "link": "queries/products-sold-today",
    },
    {
        "name": "Выручка проданного товара за февраль текущего года",
        "link": "queries/revenue-in-month",
    },
    {
        "name": "Самый популярный товар (т.е. тот товар, который продавался чаще всего)",
        "link": "queries/most-popular-product",
    },
    {
        "name": "Вывести список товаров, поставляемый Mi SHOP, отсортированный от самого дорогого до самого дешевого",
        "link": "queries/supplier-shop-products",
    },
]
