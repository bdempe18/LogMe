import subprocess
from dataclasses import asdict
from dataclasses import dataclass

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
                asdict(ConnectionTestResult.error("Connection not found")),
            )
        )

    try:
        command = conn.build_ssh_command()
        command.append('echo "Connection successful"')

        result = subprocess.run(  # noqa: S603
            command, capture_output=True, text=True, timeout=15, check=False
        )

        if result.returncode == 0:
            context = ConnectionTestResult.success(result.stdout)
        else:
            context = ConnectionTestResult.error(result.stderr)

    except subprocess.TimeoutExpired:
        context = ConnectionTestResult.error("Connection timed out after 15 seconds")
    except Exception as e:  # noqa: BLE001
        context = ConnectionTestResult.error(f"Unexpected error: {e!s}")

    html = render_to_string("components/notification.html", asdict(context))
    return HttpResponse(html)


# ---- helpers ----
@dataclass
class ConnectionTestResult:
    message: str
    success: bool

    @classmethod
    def success(cls, message: str = "Connection successful") -> "ConnectionTestResult":
        return cls(
            success=True,
            message=message,
        )

    @classmethod
    def error(cls, message: str = "Connection failed") -> "ConnectionTestResult":
        return cls(
            success=False,
            message=message,
        )
