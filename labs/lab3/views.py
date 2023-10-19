from typing import Optional

from django.db import models
from django.http import (
    HttpResponseRedirect,
    HttpResponseBadRequest,
    HttpResponseNotFound,
)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from labs.forms import table_name_to_form_map, SupplyForm, SaleForm
from labs.models import Supplier, Sale, Supply, Product

table_name_to_table_map = {
    Supplier.__name__: Supplier,
    Sale.__name__: Sale,
    Supply.__name__: Supply,
    Product.__name__: Product,
}


def table_page(request, table_name):
    table: models.Model = table_name_to_table_map.get(table_name)
    if table is None:
        return render(request, "model_data.html", {"home_link": "/labs/3/"})

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
            "home_link": "/labs/3/",
        },
    )


def entity_page(request, table_name, entity_id: Optional[int] = None):
    if not entity_id and request.method == "POST":
        form = table_name_to_form_map[table_name](request.POST)

        if form.is_valid():
            if isinstance(form, SupplyForm):
                product = Product.objects.filter(id=int(form.data["product"])).first()
                new_count = product.count + int(form.data["count"])
                product.count = new_count
                product.save()
            elif isinstance(form, SaleForm):
                product = Product.objects.filter(id=int(form.data["product"])).first()
                new_count = product.count - int(form.data["count"])
                product.count = new_count
                product.save()

            form.save()

            return HttpResponseRedirect(reverse("table", args=[table_name]))

        return render(request, "entities/entity_form.html", {"form": form})
    elif not entity_id:
        form = table_name_to_form_map[table_name]
        return render(request, "entities/entity_form.html", {"form": form})

    try:
        entity = table_name_to_table_map[table_name].objects.get(pk=entity_id)
    except Exception:
        raise HttpResponseNotFound
        # return HttpResponseRedirect(reverse("entity_not_found_view"))

    if request.method == "POST":
        form = table_name_to_form_map[table_name](request.POST, instance=entity)

        if form.is_valid():
            if isinstance(form, SupplyForm):
                product = Product.objects.filter(id=int(form.data["product"])).first()
                old_supply = Supply.objects.filter(
                    product_id=int(form.data["product"])
                ).first()
                new_count = (product.count - old_supply.count) + int(form.data["count"])
                product.count = new_count
                product.save()

            elif isinstance(form, SaleForm):
                product = Product.objects.filter(id=int(form.data["product"])).first()
                old_sale = Sale.objects.filter(
                    product_id=int(form.data["product"])
                ).first()

                new_count = (product.count + old_sale.count) - int(form.data["count"])
                product.count = new_count
                product.save()

            form.save()
            return HttpResponseRedirect(reverse("table", args=[table_name]))
    else:
        form = table_name_to_form_map[table_name](instance=entity)

    return render(request, "entities/entity_form.html", {"form": form})


def delete_entity(request, table_name: str, entity_id: int):
    entity = get_object_or_404(table_name_to_table_map[table_name], pk=entity_id)

    if request.method == "POST":
        entity.delete()
        return HttpResponseRedirect(reverse("table", args=[table_name]))

    raise HttpResponseBadRequest
