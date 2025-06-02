import subprocess
from dataclasses import dataclass


@dataclass
class ConnectionResponse:
    message: str
    is_success: bool

    @classmethod
    def success(cls, message: str = "Connection successful") -> "ConnectionResponse":
        return cls(
            is_success=True,
            message=message,
        )

    @classmethod
    def error(cls, message: str = "Connection failed") -> "ConnectionResponse":
        return cls(
            is_success=False,
            message=message,
        )


def ssh_connect(command) -> ConnectionResponse:
    try:
        result = subprocess.run(  # noqa: S603
            command, capture_output=True, text=True, timeout=15, check=False
        )

        if result.returncode == 0:
            return ConnectionResponse.success(result.stdout)
        return ConnectionResponse.error(result.stderr)
    except subprocess.TimeoutExpired:
        return ConnectionResponse.error("Connection timed out after 15 seconds")

    return ConnectionResponse.error("Unexpected Error")
