from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import lower
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from labs.forms import table_name_to_form_map
from labs.utils.model_mapping import create_model_mapping
from labs.utils.tables import table_name_to_table_map


@method_decorator(login_required, name="dispatch")
class Lab2TablePageView(ListView):
    template_name = "common/model_data.html"
    model_mapping = create_model_mapping()
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        table_name = lower(kwargs.get("slug"))
        self.model = self.model_mapping.get(table_name)
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        fields = [
            field
            for field in self.model._meta.fields
            if field.name != "id" and field.name != "deleted"
        ]
        context = {
            "model_name": self.model._meta.verbose_name,
            "hide_filter": True,
            "fields": fields,
            "home_link": "/labs/2/",
            "is_read_only": True,
        }
        kwargs.update(context)
        return super().get_context_data(object_list=None, **kwargs)


@login_required
def entity_page(request, table_name, entity_id: int | None = None):
    if not entity_id and request.method == "POST":
        form = table_name_to_form_map[table_name](request.POST)

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


@login_required
def delete_entity(request, table_name: str, entity_id: int):
    entity = get_object_or_404(table_name_to_table_map[table_name], pk=entity_id)

    if request.method == "POST":
        entity.delete()

        return HttpResponseRedirect(reverse("table", args=[table_name]))

    raise HttpResponseBadRequest
