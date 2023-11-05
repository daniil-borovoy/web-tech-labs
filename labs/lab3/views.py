from typing import Optional

from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import (
    HttpResponseRedirect,
    HttpResponseBadRequest,
    HttpResponseNotFound,
)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from labs.forms import table_name_to_form_map
from labs.utils.tables import table_name_to_table_map


@login_required
def table_page(request, table_name):
    table: models.Model = table_name_to_table_map.get(table_name)
    if table is None:
        return render(request, "common/model_data.html", {"home_link": "/labs/3/"})

    entries = table.objects.filter(deleted=False)
    fields = [f for f in table._meta.fields if f.name != "id" and f.name != "deleted"]
    return render(
        request,
        "common/model_data.html",
        {
            "model_name": table_name,
            "fields": fields,
            "data": entries,
            "hide_filter": True,
            "home_link": "/labs/3/",
        },
    )


# TODO: refactor
@login_required
def entity_page(request, table_name, entity_id: Optional[int] = None):
    form = table_name_to_form_map[table_name](request.POST)

    if not entity_id and request.method == "POST":
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("table", args=[table_name]))

        return render(request, "entities/entity_form.html", {"form": form})

    elif not entity_id:
        form = table_name_to_form_map[table_name]
        return render(request, "entities/entity_form.html", {"form": form})

    # Update entity
    try:
        entity = table_name_to_table_map[table_name].objects.get(pk=entity_id)
    except Exception:
        raise HttpResponseNotFound

    if request.method == "POST":
        form = table_name_to_form_map[table_name](request.POST, instance=entity)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("table", args=[table_name]))
    else:
        form = table_name_to_form_map[table_name](instance=entity)

    return render(request, "entities/entity_form.html", {"form": form})


@login_required
def delete_entity(request, table_name: str, entity_id: int):
    entity = get_object_or_404(table_name_to_table_map[table_name], pk=entity_id)

    if request.method == "POST":
        entity.delete()
        return HttpResponseRedirect(reverse("table", args=[table_name]))

    raise HttpResponseBadRequest
