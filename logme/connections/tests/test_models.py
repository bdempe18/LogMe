import pytest
from django.core.exceptions import ValidationError

from logme.connections import models


@pytest.fixture
def simple_connection(db):
    return models.Connection.objects.create(
        name="Test",
        password="password",  # noqa: S106
        host="101.36.40.190",
        port="12345",
        user="ben",
    )


@pytest.mark.django_db(transaction=True)
class TestConnection:
    def test_slug(self, simple_connection):
        assert simple_connection.slug == simple_connection.name.lower()

    def test_auth_method(self, simple_connection):
        assert simple_connection.auth_method == models.AuthMethod.PASSWORD

    def test_stringify(self, simple_connection):
        conn = simple_connection
        assert conn.as_str_without_port in conn.as_str

    def test_no_auth_method(self):
        with pytest.raises(ValidationError) as exc_info:
            models.Connection.objects.create(
                name="Name",
                host="101.36.40.190",
                port="12345",
                user="ben",
            )

        assert "Must provide" in str(exc_info.value)
