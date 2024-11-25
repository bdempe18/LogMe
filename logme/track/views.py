from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .models import Project

# Create your views here.


class ProjectCreateView(CreateView):
    model = Project
    template_name = "pages/projects/create.html"
    fields = ["title", "description", "log_type", "sync_command", "levels"]
    success_url = reverse_lazy("home")
