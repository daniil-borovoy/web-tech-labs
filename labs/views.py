from django.views.generic import TemplateView

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


class Lab1View(TemplateView):
    template_name = "lab1/lab1.html"


class Lab2View(TemplateView):
    template_name = "lab2/lab2.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response(context={"tables": tables, "queries": queries})


class Lab3View(TemplateView):
    template_name = "lab3/lab3.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response(context={"tables": tables})


class LabNotFoundView(TemplateView):
    template_name = "common/lab_not_found.html"


class HomeView(TemplateView):
    template_name = "home.html"


class InfoView(TemplateView):
    template_name = "info.html"


def get_lab_view_by_name(request, lab_name):
    match lab_name:
        case "1":
            return Lab1View.as_view()(request)
        case "2":
            return Lab2View.as_view()(request)
        case "3":
            return Lab3View.as_view()(request)
        case _:
            return LabNotFoundView.as_view()(request)
