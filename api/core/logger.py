from loguru import Logger
import time
from pathlib import Path


class CustomLogger(Logger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._service_name = "unknown_service"

    def get(self, service_name: str) -> "Logger":
        """
        Get the logger object.

        Returns:
            loguru.Logger: loguru logger object.

        """
        self.add(
            f"{Path(__file__).parent.parent.parent.as_posix()}/logs/{time.strftime('%Y-%m-%d')}.log",
            level="DEBUG",
            rotation="500 MB",
            compression="zip",
        )

        return self.bind(service_name=service_name)
