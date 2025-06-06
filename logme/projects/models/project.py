from django.conf import settings
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel
from django_extensions.db.models import TitleSlugDescriptionModel

from logme.connections.models import Connection

from .managers import LogManager
from .managers import ReadManager


class Project(TitleSlugDescriptionModel, TimeStampedModel, models.Model):
    log_choices = [
        ("LARAVEL", "Laravel"),
    ]

    tags = [("prod", "Production"), ("dev", "Staging"), ("local", "Local")]

    # Fields
    last_synced_at = models.DateTimeField(null=True)
    framework = models.CharField(choices=log_choices, default=log_choices[0])
    connection = models.ForeignKey(
        Connection, on_delete=models.CASCADE, null=True, blank=True
    )
    file_path = models.CharField(max_length=255)

    # regex patterns to read the first line
    pattern = models.CharField(
        max_length=255,
        blank=True,
        help_text="""
            Regex pattern needed to parse the first line of a log into the date,
            level, summary, and initial trace. The framework default will be
            used if no custom pattern is provided
        """,
    )

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.pattern:
            self.reset_pattern_to_default()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("projects:log_list", kwargs={"slug": self.slug})

    @classmethod
    def get_default_pattern(cls, framework):
        defaults = {"laravel": r"\[(.*?)\]\s[^.]+\.(\S+):\s([^{]*)(?:{?)(.*)"}

        return defaults.get(framework.lower())

    def reset_pattern_to_default(self) -> str:
        self.pattern = self.get_default_pattern(self.framework)

        return self.pattern

    @property
    def management_command(self) -> str:
        project_root = settings.BASE_DIR
        return f"cd {project_root} && poetry run python manage.py sync {self.slug}"

    @property
    def copy_command(self) -> str:
        local_dir = self.upload_directory()
        command = self.sync_command.replace("{here}", local_dir + "/")

        commands = [
            "mkdir -p " + local_dir,
            "find " + local_dir + " -mindepth 1 -delete",
            command,
            self.management_command,
        ]

        return " && ".join(commands)

    def upload_directory(self) -> str:
        return settings.MEDIA_ROOT + "/" + self.slug


class LogEntry(TimeStampedModel, models.Model):
    # Fields
    title = models.CharField(max_length=100, blank=True, default="")
    summary = models.TextField(blank=True)
    timestamp = models.DateTimeField()

    level = models.CharField(max_length=50)
    trace = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="entries",
    )

    objects = LogManager()
    read = ReadManager()

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        if self.label:
            return f"{self.label}"
        return "Log #" + self.id

    # Properties
    @property
    def label(self) -> str:
        return self.title or self.summary
