from django.urls import path

from . import views

app_name = "connections"

urlpatterns = [
    path("", views.ConnectionListView.as_view(), name="list"),
    path("create/", views.ConnectionCreateView.as_view(), name="create"),
    path("<int:pk>/", views.ConnectionDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.ConnectionUpdateView.as_view(), name="edit"),
    path("test/", views.test_connection, name="test"),
]
