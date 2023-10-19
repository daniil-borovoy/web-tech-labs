from datetime import date
from typing import Optional

from dateutil import relativedelta
from dateutil.parser import parse as parse_date
from django.db import models
from django.db.models import Count, Sum, F
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from labs.forms import table_name_to_form_map
from labs.models import Supplier, Sale, Supply, Product, Log

table_name_to_table_map = {
    Supplier.__name__: Supplier,
    Sale.__name__: Sale,
    Supply.__name__: Supply,
    Product.__name__: Product,
}


def table_page(request, table_name):
    table: models.Model = table_name_to_table_map.get(table_name)
    if table is None:
        return render(request, "model_data.html")

    entries = table.objects.filter(deleted=False)
    fields = [f for f in table._meta.fields if f.name != "id" and f.name != "deleted"]
    return render(
        request,
        "model_data.html",
        {
            "model_name": table_name,
            "fields": fields,
            "data": entries,
            "hide_filter": True,
        },
    )


def entity_page(request, table_name, entity_id: Optional[int] = None):
    if not entity_id and request.method == "POST":
        form = table_name_to_form_map[table_name](request.POST)

        # match form:
        #     case isinstance(form, Supply):
        #         product = Product.objects.filter(id=form.product_id)
        #         product.count += form.count
        #         product.save()
        #     case isinstance(form, Sale):
        #         pass
        #     case _:
        #         pass

        if form.is_valid():
            form.save()
            # Redirect to a success page or another page
            return HttpResponseRedirect(reverse("table", args=[table_name]))

        return render(
            request,
            "entities/entity_form.html",
            {"form": form, "home_link": "/labs/3/"},
        )
    elif not entity_id:
        form = table_name_to_form_map[table_name]
        return render(
            request,
            "entities/entity_form.html",
            {"form": form, "home_link": "/labs/3/"},
        )

    try:
        entity = table_name_to_table_map[table_name].objects.get(pk=entity_id)
    except Exception:
        # Handle the case when the entity doesn't exist
        return HttpResponseRedirect(reverse("entity_not_found_view"))

    if request.method == "POST":
        form = table_name_to_form_map[table_name](request.POST, instance=entity)
        if form.is_valid():
            form.save()
            # Redirect to a success page or another page
            return HttpResponseRedirect(reverse("table", args=[table_name]))
    else:
        form = table_name_to_form_map[table_name](instance=entity)

    return render(request, "entities/entity_form.html", {"form": form})


def delete_entity(request, table_name: str, entity_id: int):
    entity = get_object_or_404(table_name_to_table_map[table_name], pk=entity_id)

    if request.method == "POST":
        # entity.deleted = True
        entity.delete()

        # log = Log(data=model_to_dict(entity))
        # log.save()

        return HttpResponseRedirect(reverse("table", args=[table_name]))

    raise HttpResponseBadRequest


# Queries
def suppliers_in_city(request):
    value = (
        request.GET.get("filter_value")
        if request.GET.get("filter_value") is not None
        else "Москва"
    )
    moscow_suppliers = Supplier.objects.filter(address__icontains=value, deleted=False)
    fields = [
        f for f in Supplier._meta.fields if f.name != "id" and f.name != "deleted"
    ]

    return render(
        request,
        "model_data.html",
        {
            "model_name": f"Перечень поставщиков, расположенных по адресу в г. {value}",
            "fields": fields,
            "data": moscow_suppliers,
            "hide_filter_value": True,
        },
    )


def products_sold_in_day(request):
    # Get today's date
    today = date.today()
    fields = [f for f in Product._meta.fields if f.name != "id" and f.name != "deleted"]

    value = (
        parse_date(request.GET.get("filter_value"))
        if request.GET.get("filter_value") is not None
        and len(request.GET.get("filter_value")) > 0
        else today
    )

    # Query products sold today by filtering the Sale model
    products_sold = Product.objects.filter(sale__date=value, deleted=False)

    return render(
        request,
        "model_data.html",
        {
            "model_name": "Cписок товаров, проданных за сегодняшний день",
            "fields": fields,
            "data": products_sold,
            "input_type": "date",
            "input_value": value.strftime("%Y-%m-%d"),
            "hide_filter_value": True,
        },
    )


def revenue_in_month(request):
    february_month_number = 2
    current_year = date.today().year
    year = (
        int(request.GET.get("year"))
        if request.GET.get("year") is not None
        else current_year
    )
    month = (
        int(request.GET.get("month"))
        if request.GET.get("month") is not None
        else february_month_number
    )

    start_date = date(year, month, 1)
    end_date = start_date + relativedelta.relativedelta(months=1)

    sales_in_february = Sale.objects.filter(
        product__sale__date__range=[start_date, end_date], deleted=False
    ).annotate(revenue=Sum(F("count") * F("retail_price")))

    total_revenue = sales_in_february[0].revenue if len(sales_in_february) else 0

    return render(
        request,
        "query_3.html",
        {
            "title": "Выручка проданного товара за февраль текущего года",
            "value": total_revenue,
            "initial_year": year,
            "initial_month": month,
        },
    )


def most_popular_product(request):
    most_popular = (
        Product.objects.annotate(sales_count=Count("sale"))
        .order_by("-sales_count")
        .first()
    )

    return render(
        request,
        "one_value_display.html",
        {"title": "Самый популярный товар", "value": most_popular},
    )


def supplier_shop_products(request):
    selected_supplier = (
        request.GET.get("filter_field")
        if request.GET.get("filter_field") is not None
        else "Mi SHOP"
    )

    suppliers = Supplier.objects.all()
    ascending = (
        bool(request.GET.get("ascending"))
        if request.GET.get("ascending") is not None
        else True
    )

    mi_shop_products_data = Product.objects.filter(
        supply__supplier__name=selected_supplier, deleted=False
    ).order_by("-price")
    fields = [f for f in Product._meta.fields if f.name != "id" and f.name != "deleted"]

    return render(
        request,
        "query_5.html",
        {
            "title": f"Список товаров, поставляемый {selected_supplier}, отсортированный от самого дорогого до самого дешевого",
            "fields": fields,
            "data": mi_shop_products_data,
            "suppliers": suppliers,
            "selected_supplier": selected_supplier,
            "ascending": ascending,
        },
    )
