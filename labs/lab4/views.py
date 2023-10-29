from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView

from labs.lab4.forms import SignUpForm, SignInForm


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
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
