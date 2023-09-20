import serial
import json
import threading
from typing import Callable, Any, Dict
import base64
import random
import string
from .future import Future


class PortError(Exception):
    pass


class JSONRPC:
    """Class for sending JSONRPC messages."""

    def __init__(self) -> None:
        self._ser: serial.Serial | None = None

        self._callback_msg_filter: Callable | None = None
        self._callback_msg_dscnnctd: Callable | None = None

        self._futures = {}
        self._futures_lock = threading.Lock()

    def read_data(self) -> bytearray | None:
        if not self._ser:
            raise PortError("The port has not been defined")

        receive_buf = bytearray()
        while True:
            pos = receive_buf.find(b"\x0d")
            if pos >= 0:
                result = receive_buf[:pos]
                receive_buf = receive_buf[pos + 1 :]
                return result

            receive_buf += self._ser.read()

    def connect(self, port: serial.Serial):
        self._ser = port
        try:
            self._ser.read()
        except serial.PortNotOpenError:
            self._ser = None
            raise PortError("Unable to connect to port")

    async def request(self, method: str, params: Dict):
        if not self._ser:
            raise PortError("The port has not been defined")

        future = Future()
        msgid = self.random_id()

        jsonrpc_request = {"m": method, "p": params, "i": msgid}

        with self._futures_lock:
            self._futures[msgid] = future
        self._ser.write(json.dumps(jsonrpc_request).encode() + b"\x0D")

        return await future.result()

    def random_id(self, length: int = 4) -> str:
        return "".join(random.sample((string.ascii_letters + string.digits), length))

    def receive_forever(self) -> None:
        data = None
        while True:
            try:
                data = self.read_data()
            except serial.SerialException:
                if self._callback_msg_dscnnctd:
                    self._callback_msg_dscnnctd()
                    break
            if not data:
                break

            try:
                jsonrpc_response = json.loads(data.decode())

                with self._futures_lock:
                    if "i" in jsonrpc_response:
                        future = self._futures.get(jsonrpc_response["i"])
                    else:
                        future = None

                if future:
                    if "r" in jsonrpc_response:
                        future.set_result(jsonrpc_response["r"])
                    else:
                        future.set_exception(ValueError(jsonrpc_response["e"]))

                else:
                    if self._callback_msg_filter:
                        self._callback_msg_filter(jsonrpc_response)

            except json.JSONDecodeError:
                if self._callback_msg_filter:
                    self._callback_msg_filter(data.decode())

    def configure_callbacks(
        self,
        msg_filter: Callable[[dict], Any],
        serial_dscnnctd: Callable[[], Any],
    ):
        self._callback_msg_filter = msg_filter
        self._callback_msg_dscnnctd = serial_dscnnctd

    async def send_confirmation(self, response_id: str):
        if not self._ser:
            raise PortError("The port has not been defined")

        response = {"i": response_id}
        self._ser.write(json.dumps(response).encode() + b"\x0D")

    async def play_program(self, slot: int) -> None:
        await self.request("program_execute", {"slotid": slot})

    async def stop_program(self) -> None:
        await self.request("program_terminate", {})

    async def get_hub_info(self) -> dict:
        return await self.request("get_hub_info", {})

    async def start_write_program(
        self,
        name: str,
        size: int,
        slot: int,
        created: int,
        modified: int,
        file_name: str,
    ) -> dict:
        meta = {
            "created": created,
            "modified": modified,
            "name": str(base64.b64encode(name.encode()), "utf-8"),
            "type": "python",
            "project_id": self.random_id(12),
        }

        return await self.request(
            "start_write_program",
            {
                "slotid": slot,
                "size": size,
                "meta": meta,
                "filename": file_name,
            },
        )

    async def write_package(self, data: bytes, transfer_id: str) -> None:
        return await self.request(
            "write_package",
            {"data": str(base64.b64encode(data), "utf-8"), "transferid": transfer_id},
        )
