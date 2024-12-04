import re
from datetime import datetime

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db.models import Q
from django.utils import timezone
from Pathlib import Path

from logme.track.models import LogEntry
from logme.track.models import LogLevel
from logme.track.models import Project


class Command(BaseCommand):
    help = "Outputs sync command for a project"

    project = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.levels = LogLevel.objects.all()

    def add_arguments(self, parser):
        parser.add_argument("project_slug", type=str)

    def handle(self, *args, **options):
        try:
            self.project = Project.objects.get(slug=options["project_slug"])
        except Project.DoesNotExist as e:
            msg = f'Project {options["project_slug"]} does not exist'
            raise CommandError(msg) from e

        import os

        local_dir = self.project.upload_directory()

        if (
            not options.get("force")
            and Path.exists(local_dir)
            and not os.listdir(local_dir)
        ):
            self.ask_for_user_input()
        else:
            self.import_logs()
            self.project.last_synced_at = timezone.now()
            self.project.save()

    def ask_for_user_input(self):
        self.stdout.write(
            """
            Run the following command to sync your project.
            After running that command, run this command again to import your logs.
            """,
        )
        self.stdout.write(self.project.sync())

    def import_logs(self):
        import os

        local_dir = self.project.upload_directory()
        for filename in os.listdir(local_dir):
            self.stdout.write(f"...Importing {filename}")
            filepath = Path(local_dir) / filename
            self.import_log_from_file(filepath)

    def _extract_entry_date(
        self,
        line: str,
        start_delimiter: str = "[",
        end_delimiter: str = "]",
    ) -> datetime:
        start_index = line.find(start_delimiter) + 1
        end_index = line.find(end_delimiter)
        return datetime.strptime(line[start_index:end_index], "%Y-%m-%d %H:%M:%S%z")

    def _split_summary_and_initial_trace(
        self,
        line: str,
        split_delimiter: str = "{",
    ) -> tuple[str, str]:
        """
        Splits the line into summary and initial trace.

        Arguments:
            line: The line to split.
            split_delimiter: The delimiter to split the line on.

        Returns:
            tuple[str, str]: Summary and initial trace.
        """
        if split_delimiter in line:
            start_index = line.find(split_delimiter)
            return line[:start_index].strip(), line[start_index:].strip()
        return line.strip(), None

    def _extract_log_level(self, line: str) -> LogLevel:
        str_log_level = line.split(".")[1].split(":")[0].strip()

        return self.levels.get(title=str_log_level)

    def _extract_entry_meta_data(self, first_line: str) -> tuple[datetime, str, str]:
        """
        Uncovers the log date, log level and summary from the first line.

        Arguments:
            first_line: The first line of the log entry.

        Returns:
            tuple[datetime, str, str]: Log date, log level and summary.
        """
        log_date = self._extract_entry_date(first_line)

        post_date = " ".join(first_line.split("]")[1:]).strip()
        summary, initial_trace = self._split_summary_and_initial_trace(post_date)
        log_level = self._extract_log_level(summary)

        # we still need to remove the log level from the summary
        summary = " ".join(summary.split(".")[1:]).strip()

        return log_date, log_level, summary, initial_trace

    def read_entry(self, lines: list[str], i: int) -> tuple[LogEntry, int]:
        """
        Convert a raw log entry into a LogEntry object

        Reads a log entry from the lines and returns the log entry and the
        index of the next line.
        """
        try:
            log_date, log_level, summary, initial_trace = self._extract_entry_meta_data(
                lines[i],
            )
            trace, i = self.read_trace(lines, i, initial_trace)

            return LogEntry(
                project=self.project,
                timestamp=timezone.make_aware(log_date),
                level_id=self.levels[log_level],
                summary=summary,
                trace=trace,
            ), i
        except (ValueError, IndexError) as e:
            msg = f"Error parsing line {i}: {lines[i]}"
            raise CommandError(msg) from e

    def read_trace(
        self,
        lines: list[str],
        i: int,
        initial_trace: str,
        end_delimiter: str = '"}',
    ) -> tuple[str, int]:
        """
        Parse trace until end delimiter

        Returns:
            tuple[str, int]: The parsed trace and the index of the next line.
        """

        trace = [initial_trace] if initial_trace else []

        i += 1
        while i < len(lines) and lines[i].strip() != end_delimiter:
            trace.append(lines[i].strip() + "\n")
            i += 1

            if re.match(
                r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]",
                lines[i],
            ):
                i -= 1
                break
            trace.append(lines[i].strip() + "\n")
            i += 1

        return "\n".join(trace), i

    def import_log_from_file(self, filepath):
        logs = []

        with Path(filepath).open("r") as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                line = lines[i]

                if line.startswith("["):
                    log_entry, i = self.read_entry(lines, i)
                    logs.append(log_entry)

                i += 1

        LogEntry.objects.bulk_create(self.remove_duplicate_logs(logs))

    def remove_duplicate_logs(self, logs: list[LogEntry]) -> list[LogEntry]:
        existing_records = LogEntry.objects.filter(
            Q(summary__in=[item.summary for item in logs])
            & Q(timestamp__in=[item.timestamp for item in logs]),
        ).values_list("summary", "timestamp")

        return [
            item
            for item in logs
            if (item.summary, item.timestamp) not in existing_records
        ]
