from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.forms import DateInput
from django.utils.translation import gettext_lazy as _


class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=True)


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["username"].label = _("Username or Email")
        return form


class RegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(
        widget=DateInput(
            attrs={
                "type": "date",
                "class": "form-control"
            }
        ),
        input_formats=["%Y-%m-%d"],
        label="Date of Birth"
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        label="Email Address"
    )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})
            if field_name == "agree_terms":
                field.widget.attrs.update({"class": "form-check-input me-2"})
            if self.errors.get(field_name):
                field.widget.attrs["class"] += " is-invalid"

    agree_terms = forms.BooleanField(
        required=True,
        initial=False,
        label="I agree all statements in ",
        widget=forms.CheckboxInput(),
    )

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "date_of_birth",
            "password1",
            "password2",
        )
