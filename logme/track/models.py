from django.db import models
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel
from django_extensions.db.models import TitleSlugDescriptionModel

from .fields import HexColorField


class LogLevel(models.Model):
    title = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from=["title"])

    color_hex = HexColorField(default="COCOCO")

    def __str__(self):
        return f"{self.title}"


class Project(TitleSlugDescriptionModel, TimeStampedModel, models.Model):
    log_choices = [
        ("LARAVEL", "Laravel"),
    ]

    last_synced_at = models.DateTimeField(null=True)
    log_type = models.CharField(choices=log_choices, default=log_choices[0])
    sync_command = models.TextField(blank=True)

    levels = models.ManyToManyField(LogLevel, related_name="projects")

    def __str__(self):
        return f"{self.title}"


class LogEntry(TimeStampedModel, models.Model):
    label = models.CharField(max_length=100, default="New Log")
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="entries",
    )
    content = models.TextField()

    def __str__(self):
        if self.label:
            return f"{self.label}"

        return "Log #" + self.id
