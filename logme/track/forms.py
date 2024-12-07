from django import forms

from .models import Project


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
            "description": forms.Textarea(attrs={"rows": 3}),
            "sync_command": forms.Textarea(attrs={"rows": 5}),
            "patterns": forms.TextInput(attrs={"placeholder": "Framework default"}),
        }

    fieldsets = {
        "basic": ("title", "framework", "sync_command"),
        "advanced": ("description", "levels", "pattern"),
    }
