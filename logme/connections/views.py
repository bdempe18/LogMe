from dataclasses import asdict

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from .forms import ConnectionForm
from .models import Connection
from .utilities import ssh_connect


class ConnectionListView(ListView):
    model = Connection
    template_name = "connections/list.html"
    context_object_name = "connections"


class ConnectionCreateView(CreateView):
    model = Connection
    form_class = ConnectionForm
    template_name = "connections/form.html"
    success_url = reverse_lazy("connections:list")


class ConnectionUpdateView(UpdateView):
    model = Connection
    form_class = ConnectionForm
    template_name = "connections/form.html"
    success_url = reverse_lazy("connections:list")


class ConnectionDetailView(DetailView):
    model = Connection
    template_name = "connections/form.html"
    form_class = ConnectionForm

    def get_context_data(self, **kwargs):
        # TODO clean up with process. we can probably depend on the object pk
        # existence
        context = super().get_context_data(**kwargs)
        form = self.form_class(instance=self.object)
        # Disable all form fields
        for field in form.fields.values():
            field.widget.attrs["disabled"] = True
        context["form"] = form
        context["readonly"] = True
        return context


@require_http_methods(["POST"])
def test_connection(request):
    pk = request.POST.get("cid")

    try:
        conn = Connection.objects.get(pk=pk)
    except Connection.DoesNotExist:
        return HttpResponse(
            render_to_string(
                "components/notification.html",
                {"is_success": False, "message": "Connection not found"},
            )
        )

    command = conn.build_ssh_command()
    command.append('echo "Connection successful"')

    response = ssh_connect(command)

    html = render_to_string("components/notification.html", asdict(response))
    return HttpResponse(html)
