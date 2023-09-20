import threading
import asyncio
from typing import Any


class Future:
    def __init__(self):
        self._done = threading.Event()
        self._lock = threading.Lock()
        self._result = None
        self._exception: Exception | None = None

    async def result(self) -> Any:
        while not self._done.is_set():
            await asyncio.sleep(0)
        with self._lock:
            if self._exception:
                raise self._exception
            return self._result

    async def exception(self):
        while not self._done.is_set():
            await asyncio.sleep(0)
        with self._lock:
            return self._exception

    def set_result(self, result: Any) -> None:
        with self._lock:
            if self._done.is_set():
                raise ValueError("Future resolved already.")
            self._result = result
            self._done.set()

    def set_exception(self, exception: Exception) -> None:
        with self._lock:
            if self._done.is_set():
                raise ValueError("Future resolved already.")
            self._exception = exception
            self._done.set()
