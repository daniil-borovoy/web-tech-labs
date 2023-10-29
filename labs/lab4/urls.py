from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import SignUpView, SignInView

urlpatterns = [
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
    path("sign-in/", SignInView.as_view(), name="sign-in"),
    path("sign-out/", LogoutView.as_view(next_page="/sign-in")),
]
