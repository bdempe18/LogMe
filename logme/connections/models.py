from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

LOCAL_PATH = "{here}"


class Connection(models.Model):
    name = models.CharField(max_length=255)
    identity_file = models.FilePathField(
        path="/",
        match=r".*\.pem$",
        recursive=True,
        max_length=255,
    )

    password = models.CharField(
        max_length=255,
        help_text="""
            Password for authentication.
            Required if no identity file is provided.
        """,
    )

    host = models.GenericIPAddressField()
    port = models.PositiveIntegerField()
    user = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("connections:detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse("connections:edit", kwargs={"pk": self.pk})

    def clean(self):
        if not self.identity_file and not self.password:
            err = "Must provide either password or identity file"
            raise ValidationError(err)

        if self.identity_file and self.password:
            err = "Cannot provide both password and identity file"
            raise ValidationError(err)

    def connection_string(self) -> str:
        return f"{self.user}@{self.host}:{self.port}"
