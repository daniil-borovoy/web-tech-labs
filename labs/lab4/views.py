from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Model
from django.forms.utils import ErrorList
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, TemplateView, ListView

from labs.lab4.forms import SignUpForm, SignInForm
from labs.models import Supplier, Product, Supply, Sale, Log
from labs.utils.model_mapping import create_model_mapping
from labs.utils.permissions import get_admin_module_permissions


class SignUpView(CreateView):
    template_name = "auth/sign_up.html"
    form_class = SignUpForm
    success_url = reverse_lazy("sign-in")

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
        else:
            errors = form._errors.setdefault("username", ErrorList())
            errors.append(
                "Пользователь не найден или введен неверный пароль! Проверьте правильность логина и пароля"
            )
            return super().form_invalid(form)


tables_to_show = [Supplier, User, Log, Sale, Supply, Product]

menu_data = [
    {
        "name": model._meta.verbose_name_plural.capitalize(),
        "model_name": model._meta.model_name + "/1",
    }
    for model in tables_to_show
]


class AdminModuleView(PermissionRequiredMixin, TemplateView):
    template_name = "auth/auth_base.html"

    permission_required = get_admin_module_permissions()

    def get(self, request, *args, **kwargs):
        return self.render_to_response({"tables_list": menu_data})


class AdminTableView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = "lab4/model_table.html"
    model_mapping = create_model_mapping()
    permission_required = get_admin_module_permissions()
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        table_name = kwargs.get("table_name")
        self.model: Model = self.model_mapping.get(table_name)
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        fields = [
            field
            for field in self.model._meta.fields
            if field.name != "id"
            and field.name != "deleted"
            and field.name != "password"
        ]
        context = {
            "model_name": self.model._meta.model_name,
            "i18n_name": self.model._meta.verbose_name_plural,
            "hide_filter": True,
            "fields": fields,
            "home_link": "/admin-module/",
        }
        kwargs.update(context)
        return super().get_context_data(object_list=None, **kwargs)
