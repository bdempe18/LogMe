from django.urls import path

from .views import LogDetailView
from .views import ProjectCreateView
from .views import log_entry_delete
from .views import log_entry_list

app_name = "projects"

urlpatterns = [
    path("create/", ProjectCreateView.as_view(), name="create"),
    path("view/<slug:slug>/", log_entry_list, name="log_list"),
    path("log/<int:pk>/", LogDetailView.as_view(), name="log_detail"),
    path("log-entries/<int:pk>/delete/", log_entry_delete, name="log_entry_delete"),
]
