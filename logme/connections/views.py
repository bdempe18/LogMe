from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from .forms import ConnectionForm
from .models import Connection


class ConnectionListView(ListView):
    model = Connection
    template_name = "connections/list.html"
    context_object_name = "connections"


class ConnectionCreateView(CreateView):
    model = Connection
    form_class = ConnectionForm
    template_name = "connections/form.html"
    success_url = reverse_lazy("connection:list")


class ConnectionUpdateView(UpdateView):
    model = Connection
    form_class = ConnectionForm
    template_name = "connections/form.html"
    success_url = reverse_lazy("connection:list")


class ConnectionDetailView(DetailView):
    model = Connection
    template_name = "connections/form.html"
    form_class = ConnectionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.form_class(instance=self.object)
        # Disable all form fields
        for field in form.fields.values():
            field.widget.attrs["disabled"] = True
        context["form"] = form
        context["readonly"] = True
        return context
