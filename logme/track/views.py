from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .filters import LogEntryFilter
from .forms import ProjectForm
from .models import LogEntry
from .models import Project


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/create.html"
    success_url = reverse_lazy("home")


class ProjectLogs(ListView):
    model = LogEntry
    template_name = "projects/list.html"
    context_object_name = "entries"
    paginate_by = 25
    filterset_class = LogEntryFilter

    def get_queryset(self):
        slug = self.kwargs["slug"]

        project = Project.objects.get(slug=slug)
        queryset = LogEntry.objects.prefetch_related("level").filter(project=project)

        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset

        return context


class LogDetailView(DetailView):
    model = LogEntry
    template_name = "projects/log_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trace"] = self.object.trace.split("\n") if self.object.trace else []
        context["supressing_keywords"] = "/vendor/"
        return context


@require_http_methods(["DELETE"])
def log_entry_delete(request, pk):
    entry = get_object_or_404(LogEntry, pk=pk)
    entry.delete()

    return HttpResponse(status=204)
