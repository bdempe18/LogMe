from django import forms
from django.contrib.contenttypes.models import ContentType

from logme.connections.models import Connection

from .models import Project


def placeholder(placeholder_text: str) -> forms.TextInput:
    return forms.TextInput(attrs={"placeholder": placeholder_text})


class ProjectForm(forms.ModelForm):
    connection = forms.ModelChoiceField(
        queryset=Connection.objects.all(), required=False, empty_label="Local"
    )

    class Meta:
        model = Project
        fields = ["title", "framework", "description", "pattern", "file_path"]

        widgets = {
            "title": placeholder("My Project"),
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "A beautiful panda TUI image generator",
                }
            ),
            "pattern": placeholder("Framework default"),
        }

    fieldsets = {
        "basic": ("title", "framework", "file_path", "connection"),
        "advanced": ("description", "pattern"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set initial connection if instance exists
        if self.instance and self.instance.pk and self.instance.connection:
            self.fields["connection"].initial = self.instance.connection

    def save(self, commit=True):  # noqa: FBT002
        instance = super().save(commit=False)

        # Set the connection
        connection = self.cleaned_data["connection"]
        if connection:
            instance.content_type = ContentType.objects.get_for_model(
                connection.__class__
            )
            instance.object_id = connection.id
        else:
            instance.content_type = None
            instance.object_id = None

        if commit:
            instance.save()
        return instance
