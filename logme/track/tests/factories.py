import random
from datetime import UTC

from factory import Faker
from factory import LazyAttribute
from factory import SubFactory
from factory.django import DjangoModelFactory

from logme.track.models import LogEntry
from logme.track.models import LogLevel
from logme.track.models import Project


class ProjectFactory(DjangoModelFactory[Project]):
    title = Faker("sentence", nb_words=3)
    sync_command = Faker("sentence", nb_words=25)
    framework = "LARAVEL"

    class Meta:
        model = Project


class LogEntryFactory(DjangoModelFactory[LogEntry]):
    title = Faker("sentence", nb_words=3)
    summary = Faker("sentence", nb_words=15)
    trace = Faker("sentence", nb_words=100)
    project = SubFactory(ProjectFactory)
    timestamp = Faker("date_time_this_year", before_now=True, tzinfo=UTC)

    @LazyAttribute
    def level(self):
        return random.choice(LogLevel.objects.all())  # noqa: S311

    class Meta:
        model = LogEntry
