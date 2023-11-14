from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.http import (
    HttpResponseRedirect,
    HttpResponseBadRequest,
    HttpResponseNotFound,
)
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import lower
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from labs.forms import table_name_to_form_map
from labs.utils.model_mapping import create_model_mapping
from labs.utils.tables import table_name_to_table_map


@method_decorator(login_required, name="dispatch")
class Lab3TableView(ListView):
    template_name = "lab4/model_table.html"
    model_mapping = create_model_mapping()
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        table_name = lower(kwargs.get("table_name"))
        self.model: Model = self.model_mapping.get(table_name)
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        fields = [
            field
            for field in self.model._meta.fields
            if field.name != "id" and field.name != "deleted"
        ]
        context = {
            "model_name": self.model._meta.model_name,
            "i18n_name": self.model._meta.verbose_name,
            "hide_filter": True,
            "fields": fields,
            "home_link": "/labs/3/",
        }
        kwargs.update(context)
        return super().get_context_data(object_list=None, **kwargs)


# TODO: refactor
@login_required
def entity_page(request, table_name, entity_id: int | None = None):
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
