import pytest
from django.utils.text import slugify

from logme.track import models as track


@pytest.mark.django_db
class TestLogLevel:
    def test_str(self):
        title = "this is a test"
        level = track.LogLevel(title=title, slug=slugify(title))

        assert str(level) == title
