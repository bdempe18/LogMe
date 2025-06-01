import enum

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

LOCAL_PATH = "{here}"
CONNECTION_TIMEOUT = 10


class AuthMethod(enum.Enum):
    PASSWORD = "password"  # noqa: S105
    IDENTITY_FILE = "identity_file"


# blank=True is not usually a good practice for charfields and other db fields,
# but im using null to signal which auth method is being used
class Connection(models.Model):
    name = models.CharField(max_length=255)
    identity_file = models.FilePathField(  # noqa: DJ001
        path="/",
        match=r".*\.pem$",
        recursive=True,
        max_length=255,
        blank=False,
        null=True,
    )

    password = models.CharField(  # noqa: DJ001
        max_length=255,
        help_text="""
            Password for authentication.
            Required if no identity file is provided.
        """,
        blank=False,
        null=True,
    )

    host = models.GenericIPAddressField()
    port = models.PositiveIntegerField()
    user = models.CharField(max_length=50)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("connections:detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse("connections:edit", kwargs={"pk": self.pk})

    def build_ssh_command(self):
        command = ["ssh"]
        command.extend(["-o", f"ConnectTimeout={CONNECTION_TIMEOUT}"])

        if self.auth_method == AuthMethod.IDENTITY_FILE and self.identity_file:
            command.extend(["-i", self.identity_file])
        elif self.auth_method == AuthMethod.PASSWORD and self.password:
            command = ["sshpass", "-p", self.password, *command]

        # Add user and host
        command.extend(["-p", str(self.port)])
        command.append(self.as_str_without_port)

        return command

    @property
    def auth_method(self) -> AuthMethod:
        if self.identity_file:
            return AuthMethod.IDENTITY_FILE
        return AuthMethod.PASSWORD

    @property
    def as_str_without_port(self) -> str:
        return f"{self.user}@{self.host}"

    @property
    def as_str(self) -> str:
        return f"{self.as_str_without_port}:{self.port}"

    def clean(self):
        if not self.identity_file and not self.password:
            err = "Must provide either password or identity file"
            raise ValidationError(err)

        if self.identity_file and self.password:
            err = "Cannot provide both password and identity file"
            raise ValidationError(err)
