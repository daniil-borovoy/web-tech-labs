from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, MinLengthValidator
from django.utils.translation import gettext as _

from labs.lab4.input_widget import TextInputWidget


class SignInForm(forms.Form):
    username: str = forms.CharField(
        required=True,
        label="Логин",
        widget=TextInputWidget(input_type="text"),
        max_length=255,
    )
    password: str = forms.CharField(
        max_length=255,
        label="Пароль",
        widget=TextInputWidget(
            input_type="text",
        ),
    )


class SignUpForm(forms.ModelForm):
    repeat_password = forms.CharField(
        label="Повтор пароля",
        widget=TextInputWidget(
            input_type="text",
        ),
        max_length=255,
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget = TextInputWidget(
            input_type="text",
        )
        self.fields["username"].label = "Логин"
        self.fields[
            "username"
        ].help_text = "150 символов или меньше. Только буквы, цифры и @/./+/-/_."

        self.fields["first_name"].widget = TextInputWidget(
            label="Имя",
            input_type="text",
        )
        self.fields["first_name"].label = "Имя"
        self.fields["first_name"].required = True
        self.fields["first_name"].validators.append(
            MinLengthValidator(limit_value=5, message="Введите минимум 5 символов!")
        )

        self.fields["last_name"].widget = TextInputWidget(
            label="Фамилия",
            input_type="text",
        )
        self.fields["last_name"].label = "Фамилия"
        self.fields["last_name"].required = True
        self.fields["last_name"].validators.append(
            MinLengthValidator(limit_value=5, message="Введите минимум 5 символов!")
        )

        self.fields["email"].widget = TextInputWidget(
            input_type="email",
        )
        self.fields["email"].label = "Email"
        self.fields["email"].validators[0] = EmailValidator(
            message="Введите верный email!"
        )

        self.fields["password"].widget = TextInputWidget(
            input_type="text",
        )
        self.fields["password"].max_length = 255
        self.fields["password"].label = "Пароль"
        self.fields["password"].validators.append(
            MinLengthValidator(limit_value=8, message="Введите минимум 8 символов!")
        )
        self.fields["password"].help_text = "Минимум 8 символов"

        test = self.fields
        print(test)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")

        if password and repeat_password and password != repeat_password:
            raise ValidationError(
                _("Passwords didn't happen. Please check if your input is correct!")
            )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
