from django.urls import path

from .views import LogDetailView
from .views import ProjectCreateView
from .views import ProjectLogs
from .views import log_entry_delete

app_name = "projects"

urlpatterns = [
    path("create/", ProjectCreateView.as_view(), name="create"),
    path("view/<slug:slug>/", ProjectLogs.as_view(), name="list"),
    path("log/<int:pk>/", LogDetailView.as_view(), name="log_detail"),
    path("log-entries/<int:pk>/delete/", log_entry_delete, name="log_entry_delete"),
]
