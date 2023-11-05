from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, CreateView, TemplateView, ListView

from labs.lab4.forms import SignUpForm, SignInForm
from labs.utils.model_mapping import create_model_mapping, get_all_model_meta_names


class SignUpView(CreateView):
    template_name = "auth/sign_up.html"
    form_class = SignUpForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = form.cleaned_data["username"]
        user.set_password(form.cleaned_data["password"])
        user.save()
        login(self.request, user)
        return super().form_valid(form)


class SignInView(FormView):
    template_name = "auth/sign_in.html"
    form_class = SignInForm
    success_url = reverse_lazy("sign-in")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class AdminModuleView(TemplateView):
    template_name = "auth/auth_base.html"

    def get(self, request, *args, **kwargs):
        table_names = get_all_model_meta_names()
        return self.render_to_response({"tables_list": table_names})


@method_decorator(login_required, name="dispatch")
class AdminTableView(ListView):
    template_name = "lab4/model_table.html"
    model_mapping = create_model_mapping()
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        table_name = kwargs.get("table_name")
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
            "hide_filter": True,
            "fields": fields,
            "home_link": "/admin-module/",
        }
        kwargs.update(context)
        return super().get_context_data(object_list=None, **kwargs)


# def create_admin_entity_view(request, table_name, entity_id: int | None = None):
#     form = table_model_name_to_form_map[table_name](request.POST)
#
#     if not entity_id and request.method == "POST":
#         if form.is_valid():
#             form.save()
#
#             return HttpResponseRedirect(reverse("table", args=[table_name]))
#
#         return render(request, "entities/entity_form.html", {"form": form})
#
#     elif not entity_id:
#         form = table_model_name_to_form_map[table_name]
#         return render(request, "entities/entity_form.html", {"form": form})
#
#     # Update entity
#     try:
#         entity = table_name_to_table_map[table_name].objects.get(pk=entity_id)
#     except Exception:
#         raise HttpResponseNotFound
#
#     if request.method == "POST":
#         form = table_model_name_to_form_map[table_name](request.POST, instance=entity)
#
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("table", args=[table_name]))
#     else:
#         form = table_model_name_to_form_map[table_name](instance=entity)
#
#     return render(request, "entities/entity_form.html", {"form": form})
