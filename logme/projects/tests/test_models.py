import pytest
from django.utils.text import slugify

from logme.projects import models


@pytest.mark.django_db
class TestLogLevel:
    def test_str(self):
        title = "this is a test"
        level = models.LogLevel(title=title, slug=slugify(title))

        assert str(level) == title
