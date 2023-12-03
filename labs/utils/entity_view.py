from typing import Type

from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from labs.forms import table_model_name_to_form_map
from labs.utils.model_mapping import create_model_mapping


@login_required
def create_add_view(request, table_name: str):
    model_mapping = create_model_mapping()
    model: Model = model_mapping.get(table_name)
    form_class = table_model_name_to_form_map.get(model._meta.model_name)
    return AddEntityView.as_view(
        model=model, form_class=form_class, table_name=table_name
    )(request)


@login_required
def create_edit_view(request, table_name: str, entity_id: int):
    model_mapping = create_model_mapping()
    model: Model = model_mapping.get(table_name)
    form_class = table_model_name_to_form_map.get(model._meta.model_name)
    return EditEntityView.as_view(
        model=model, form_class=form_class, entity_id=entity_id, table_name=table_name
    )(request)


@login_required
def create_delete_view(request, table_name: str, pk: int):
    model_mapping = create_model_mapping()
    model: Model = model_mapping.get(table_name)
    entity = model.objects.filter(pk=pk)
    entity.delete()
    return HttpResponseRedirect(reverse("admin-table", args=[table_name]))


class AddEntityView(CreateView):
    template_name = "entities/entity_form.html"
    table_name = None

    def __init__(
        self, model: Type[Model], form_class: Type[ModelForm], table_name: str
    ):
        self.model = model
        self.success_url = f"/admin-module/{table_name}/"
        self.form_class = form_class
        super().__init__()

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs.update({"home_link": f"/admin-module/{self.model._meta.model_name}/1"})
        return super().get_context_data(object_list=None, **kwargs)


class EditEntityView(UpdateView):
    template_name = "entities/entity_form.html"
    table_name = None
    entity_id = None

    def __init__(
        self,
        model: Type[Model],
        form_class: Type[ModelForm],
        table_name: str,
        entity_id: int,
    ):
        self.model = model
        self.fields = model._meta.fields
        self.form_class = form_class
        self.table_name = table_name
        self.entity_id = entity_id
        super().__init__()

    def get(self, request, *args, **kwargs):
        entity = self.model.objects.get(pk=self.entity_id)
        form = self.form_class(instance=entity)
        return self.render_to_response(
            {"form": form, "home_link": f"/admin-module/{self.table_name}/1"}
        )

    def post(self, request, *args, **kwargs):
        try:
            entity = self.model.objects.get(pk=self.entity_id)
        except Exception:
            raise HttpResponseNotFound

        form = self.form_class(request.POST, instance=entity)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin-table", args=[self.table_name]))

        return self.render_to_response(
            {"form": form, "home_link": f"/admin-module/{self.table_name}/1"}
        )
