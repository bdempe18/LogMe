from django.urls import path

from .views import ConnectionCreateView
from .views import ConnectionDetailView
from .views import ConnectionListView
from .views import ConnectionUpdateView

app_name = "connections"

urlpatterns = [
    path("new/", ConnectionCreateView.as_view(), name="create"),
    path("edit/<int:pk>", ConnectionUpdateView.as_view(), name="edit"),
    path("<int:pk>", ConnectionDetailView.as_view(), name="detail"),
    path("", ConnectionListView.as_view(), name="list"),
]
