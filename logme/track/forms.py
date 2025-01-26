from django import forms

from .models import LogLevel
from .models import Project


def placeholder(placeholder_text: str) -> forms.TextInput:
    return forms.TextInput(attrs={"placeholder": placeholder_text})


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "framework",
            "description",
            "levels",
            "pattern",
            "sync_command",
        ]

        widgets = {
            "title": placeholder("My Project"),
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "A beautiful panda TUI image generator",
                }
            ),
            "sync_command": forms.Textarea(
                attrs={"rows": 5, "placeholder": "cp localproject {here}"}
            ),
            "pattern": placeholder("Framework default"),
        }

    fieldsets = {
        "basic": ("title", "framework", "sync_command"),
        "advanced": ("description", "levels", "pattern"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["levels"].initial = [lev.pk for lev in LogLevel.objects.all()]
