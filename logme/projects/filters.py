import django_filters as df

from .models import LogEntry


class LogEntryFilter(df.FilterSet):
    timestamp = df.DateTimeFromToRangeFilter(
        widget=df.widgets.RangeWidget(
            attrs={
                "type": "date",
            }
        ),
        label="Timestamp range",
    )

    summary = df.CharFilter(lookup_expr="icontains")

    class Meta:
        model = LogEntry
        fields = ["summary", "timestamp"]
