from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView
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


def log_entry_list(request, slug):
    project = Project.objects.get(slug=slug)
    entries = project.entries.prefetch_related("level")

    filterset = LogEntryFilter(request.GET, queryset=entries)

    paginator = Paginator(filterset.qs, 25)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {"entries": page_obj, "project": project, "filterset": filterset}

    if request.headers.get("HX-Request"):
        return render(request, "projects/_log_list.html", context)

    return render(request, "projects/list.html", context)


class LogDetailView(DetailView):
    model = LogEntry
    template_name = "projects/log_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trace"] = self.object.trace.split("\n") if self.object.trace else []
        context["supressing_keywords"] = "/vendor/"
        context["n_related"] = (
            LogEntry.objects.filter(summary=self.object.summary)
            .exclude(pk=self.object.pk)
            .count()
        )
        return context

    def get(self, request, *args, **kwargs):
        log = self.get_object()

        if not log.is_read:
            log.is_read = True
            log.save()

        return super().get(request, *args, **kwargs)


@require_http_methods(["DELETE"])
def log_entry_delete(request, pk):
    entry = get_object_or_404(LogEntry, pk=pk)
    entry.delete()

    return HttpResponse(status=204)
