from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from labs.lab4.input_widget import TextInputWidget


class SignInForm(forms.Form):
    username: str = forms.CharField(
        required=True,
        widget=TextInputWidget(label="Username", input_type="text"),
        max_length=255,
    )
    password: str = forms.CharField(
        max_length=255,
        widget=TextInputWidget(
            label="Password",
            input_type="text",
        ),
    )


class SignUpForm(forms.ModelForm):
    repeat_password = forms.CharField(
        widget=TextInputWidget(
            label="Repeat Password",
            input_type="password",
        ),
        max_length=255,
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Specify the widget for selected fields
        self.fields["username"].widget = TextInputWidget(
            label="Username",
            input_type="text",
        )

        self.fields["first_name"].widget = TextInputWidget(
            label="First Name",
            input_type="text",
        )

        self.fields["last_name"].widget = TextInputWidget(
            label="Last Name",
            input_type="text",
        )

        self.fields["email"].widget = TextInputWidget(
            label="Email",
            input_type="email",
        )

        self.fields["password"].widget = TextInputWidget(
            label="Password",
            input_type="password",
        )
        self.fields["password"].max_length = 255

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")

        if password and repeat_password and password != repeat_password:
            raise ValidationError(
                "Passwords do not match. Please enter the same password in both fields."
            )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
