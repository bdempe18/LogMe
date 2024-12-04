from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from .models import LogEntry
from .models import Project


class ProjectCreateView(CreateView):
    model = Project
    template_name = "pages/projects/create.html"
    fields = ["title", "description", "log_type", "sync_command", "levels"]
    success_url = reverse_lazy("home")


class ProjectDetailView(DetailView):
    model = Project
    template_name = "pages/projects/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entries"] = (
            self.object.entries.all().prefetch_related("level").order_by("-timestamp")
        )
        return context


class LogDetailView(DetailView):
    model = LogEntry
    template_name = "pages/projects/log_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trace"] = self.object.trace.split("\n") if self.object.trace else []
        context["supressing_keywords"] = "/vendor/"
        return context


@require_http_methods(["DELETE"])
def log_entry_delete(request, pk):
    entry = get_object_or_404(LogEntry, pk=pk)
    entry.delete()

    return HttpResponse(status=200)
