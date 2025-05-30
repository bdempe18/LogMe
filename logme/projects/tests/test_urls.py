from http import HTTPStatus

import pytest
from django.urls import resolve
from django.urls import reverse

from logme.projects import views
from logme.projects.models import LogEntry

from .factories import LogEntryFactory
from .factories import ProjectFactory


@pytest.mark.django_db
class TestProjects:
    def check_url(self, client, view, expected, **kwargs):
        url = reverse(view, kwargs=kwargs)
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert resolve(url).func.view_class == expected

    def test_create(self, client):
        self.check_url(client, "projects:create", views.ProjectCreateView)

    def test_log_list(self, client):
        project = ProjectFactory()

        self.check_url(
            client, "projects:log_list", views.log_entry_list(), slug=project.slug
        )

    def test_log_detail(self, client):
        log = LogEntryFactory()
        self.check_url(client, "projects:log_detail", views.LogDetailView, pk=log.pk)

    def test_log_delete(self, client):
        log = LogEntryFactory()
        pk = log.pk

        url = reverse("projects:log_entry_delete", kwargs={"pk": log.pk})
        response = client.delete(url)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert not LogEntry.objects.filter(pk=pk).exists()

    def test_bad_log_delete(self, client):
        log = LogEntryFactory()
        pk = log.pk
        log.delete()

        url = reverse("projects:log_entry_delete", kwargs={"pk": pk})
        response = client.delete(url)

        assert response.status_code == HTTPStatus.NOT_FOUND
