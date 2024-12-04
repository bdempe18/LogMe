from django.urls import path

from .views import LogDetailView
from .views import ProjectCreateView
from .views import ProjectDetailView
from .views import log_entry_delete

app_name = "projects"

urlpatterns = [
    path("create/", ProjectCreateView.as_view(), name="create"),
    path("view/<slug:slug>/", ProjectDetailView.as_view(), name="detail"),
    path("log/<int:pk>/", LogDetailView.as_view(), name="log_detail"),
    path("log-entries/<int:pk>/delete/", log_entry_delete, name="log_entry_delete"),
]
