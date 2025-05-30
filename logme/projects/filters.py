import django_filters as df
from django import forms

from .models import LogEntry
from .models import LogLevel


class LogEntryFilter(df.FilterSet):
    timestamp = df.DateTimeFromToRangeFilter(
        widget=df.widgets.RangeWidget(
            attrs={
                "type": "date",
            }
        ),
        label="Timestamp range",
    )

    level = df.ModelMultipleChoiceFilter(
        queryset=LogLevel.objects.distinct(),
        widget=forms.CheckboxSelectMultiple(),
        label="Log Level",
    )

    summary = df.CharFilter(lookup_expr="icontains")

    class Meta:
        model = LogEntry
        fields = ["summary", "timestamp", "level"]
