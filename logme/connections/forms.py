from django import forms
from django.core.exceptions import ValidationError

from .models import Connection


class ConnectionForm(forms.ModelForm):
    auth_method = forms.ChoiceField(
        choices=[("key", "SSH Key"), ("password", "Password")],
        initial="key",
        widget=forms.RadioSelect(
            attrs={"class": "flex gap-4", "x-model": "authMethod"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"x-show": 'authMethod === "password"', "x-cloak": True}
        ),
        required=False,
        help_text="Required if using password authentication",
    )

    class Meta:
        model = Connection
        fields = ["name", "host", "port", "user", "identity_file", "password"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "host": forms.TextInput(attrs={"class": "form-control"}),
            "port": forms.TextInput(attrs={"class": "form-control"}),
            "user": forms.TextInput(attrs={"class": "form-control"}),
            "identity_file": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "x-show": 'authMethod === "key"',
                    "x-cloak": True,
                }
            ),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial auth method based on existing data
        if self.instance and self.instance.pk:
            self.fields["auth_method"].initial = (
                "password" if self.instance.password else "key"
            )

        # Make fields required based on auth method
        self.fields["identity_file"].required = False
        self.fields["password"].required = False

        # Reorder fields to show auth method first
        self.fieldsets = {
            "authentication": ["auth_method", "identity_file", "password"],
            "connection": ["name", "host", "port", "user"],
        }

    def clean_identity_file(self):
        return self.cleaned_data.get("identity_file")

    def clean(self):
        cleaned_data = super().clean()
        auth_method = cleaned_data.get("auth_method")
        identity_file = cleaned_data.get("identity_file")
        password = cleaned_data.get("password")

        if auth_method == "key" and not identity_file:
            err = "Please select an identity file for key authentication."
            raise ValidationError(err)
        if auth_method == "password" and not password:
            err = "Please provide a password for password authentication."
            raise ValidationError(err)

        # Clear the unused authentication field
        if auth_method == "key":
            cleaned_data["password"] = None
        else:
            cleaned_data["identity_file"] = None

        return cleaned_data
