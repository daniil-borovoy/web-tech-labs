from django.shortcuts import render

from labs.models import Product, Supplier, Sale, Supply

tables = [
    {"name": "Поставщики", "link": f"tables/{Supplier.__name__}"},
    {"name": "Продажи", "link": f"tables/{Sale.__name__}"},
    {"name": "Поставки", "link": f"tables/{Supply.__name__}"},
    {"name": "Товары", "link": f"tables/{Product.__name__}"},
]

queries = [
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


def handle_lab_1(request, lab_number):
    product = None
    if request.method == "POST":
        product = Product(
            name=request.POST["name"],
            receipt_date=request.POST["receipt_date"],
            count=request.POST["count"],
            price=request.POST["price"],
        )
    return render(request, f"lab{lab_number}.html", context={"product": product})


def handle_lab_1_2(request, lab_number):
    supplier = None
    if request.method == "POST":
        supplier = Supplier(
            name=request.POST["name"],
            who_to_contact=request.POST["who_to_contact"],
            address=request.POST["who_to_contact"],
            phone=request.POST["phone"],
        )
    return render(request, f"lab{lab_number}.html", context={"supplier": supplier})


def handle_lab_2(request, lab_number):
    return render(
        request, f"lab{lab_number}.html", {"tables": tables, "queries": queries}
    )


def handle_lab_3(request, lab_number):
    return render(request, f"lab{lab_number}.html", {"tables": tables})


def default_handler(request, lab_number):
    return render(request, f"lab{lab_number}.html")
