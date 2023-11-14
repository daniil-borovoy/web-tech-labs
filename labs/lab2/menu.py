from labs.models import Supplier, Sale, Supply, Product

menu_tables = [
    {"name": "Поставщики", "link": f"tables/{Supplier._meta.model_name}"},
    {"name": "Продажи", "link": f"tables/{Sale._meta.model_name}"},
    {"name": "Поставки", "link": f"tables/{Supply._meta.model_name}"},
    {"name": "Товары", "link": f"tables/{Product._meta.model_name}"},
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
