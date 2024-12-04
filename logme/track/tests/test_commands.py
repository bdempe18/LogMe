from datetime import datetime

import pytest

from logme.track.management.commands.sync import Command
from logme.track.models import LogLevel


@pytest.fixture(
    params=[
        # normal first line of a log
        "[2024-11-16 18:15:59] local.ERROR: SQLSTATE[42S21]: Column already exists: "
        "1060 Duplicate column name 'file_record_id' (Connection: mysql, SQL: alter "
        "table `sga_submissions` add `file_record_id` bigint unsigned null) "
        '{"exception":"[object] (Illuminate\\\\Database\\\\QueryException(code: 42S21): '  # noqa: E501
        "SQLSTATE[42S21]: Column already exists: 1060 Duplicate column name "
        "'file_record_id' (Connection: mysql, SQL: alter table `sga_submissions` add "
        "`file_record_id` bigint unsigned null) at "
        "/var/www/html/vendor/laravel/framework/src/Illuminate/Database/Connection.php:829)",
        # test odd spacing
        ' [2024-11-16 18:10:17] local.ERROR: Class "Laravel\\Horizon\\'
        'HorizonApplicationServiceProvider" not found {"exception":"[object] '
        '(Error(code: 0): Class "Laravel\\\\Horizon\\\\HorizonApplicationServiceProvider" '  # noqa: E501
        'not found at /var/www/html/app/Providers/HorizonServiceProvider.php:9}"',
        '[2024-08-16 14:15:45] local.INFO: CMTE {"message":{"To":"dempe18@gmail.com",'
        # test email log
        '"Data":{"verify_email_link":"https://alzportal.ddev.site/email/verify/8/'
        "b8bad48f516fa3bf8a73e0818c520e65a4f46de9?expires=1723819545&signature="
        '1a6e8fd75c2f7a11ce0df2aa62b88d0cd4d36df7325a24b0e6e7a4495a633a87",'
        '"user":"Ben"},"CC":[],"BCC":[]}}',
    ],
)
def first_line(request):
    return request.param


@pytest.mark.parametrize(
    ("expected_summary", "expected_trace"),
    [
        ("There is no delimiter in this line", ""),
        ("This line has a simple summary ", "{ and the start of a trace"),
        ("This line has a summary with a delimiter ", "{ and a trace and an end }"),
        (
            "This line has a summary with a delimiter ",
            "{ and a trace { and a second trace",
        ),
        ("this line has a ", "{ lot of } special @ characters # this ...%"),
    ],
)
@pytest.mark.django_db
def test_extract_summary(expected_summary, expected_trace):
    """Make sure that command can split a line into summary and initial trace value."""
    command = Command()

    line = expected_summary + expected_trace

    test_summary, test_trace = command._split_summary_and_initial_trace(line)

    # we need to correctly assert for empty trace
    expected_trace = None if expected_trace == "" else expected_trace.strip()

    assert test_summary == expected_summary.strip()
    assert test_trace == expected_trace


@pytest.mark.django_db
def test_extract_date(first_line):
    """Make sure that command can extract the date from the first line."""
    command = Command()

    start_index = first_line.find("[")
    end_index = first_line.find("]")
    date_string = first_line[start_index + 1 : end_index]
    date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")  # noqa: DTZ007

    try:
        test_date = command._extract_entry_date(first_line)
    except ValueError as e:
        pytest.fail(f"Failed to parse date: {e}")

    assert date == test_date


@pytest.mark.django_db
def test_extract_log_level(first_line):
    """Make sure that command can extract the log level from the first line."""
    command = Command()

    try:
        log_level = command._extract_log_level(first_line)
    except ValueError:
        pytest.fail("Unknown log level")

    assert isinstance(log_level, LogLevel)
    assert log_level.pk is not None

    # there is a slight risk since im not actually confirming
    # that the log level is correct
