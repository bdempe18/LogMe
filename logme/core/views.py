from django.shortcuts import render

from logme.projects.models import Project


def home(request):
    projects = Project.objects.order_by("title").all()

    return render(request, "pages/home.html", {"projects": projects})
