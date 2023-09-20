import threading
import serial
import tkinter as tk
import tkinter.messagebox as tkm
import base64
import mpy_cross_v5
import functools
import textwrap
import time
import serial.tools.list_ports
import threading
from io import StringIO, BytesIO
from typing import Callable
import queue
from async_tkinter_loop.mixins import AsyncTk
from async_tkinter_loop import async_handler

from .interface import ProgramControl, Terminal, HubStatus
from .jsonrpc import JSONRPC


class App(tk.Tk, AsyncTk):
    """GUI that allows you to control and upload programs to
    the Lego Robot Inventor (51515) hub and the SPIKE Prime (45678) hub.
    """

    def __init__(self):
        super().__init__()

        self._ser = serial.Serial()
        self._rpc = JSONRPC()
        self._interface_queue = queue.Queue()

        # Configure the JSONRPC
        self._rpc.configure_callbacks(
            msg_filter=self._filter_messages,
            serial_dscnnctd=lambda: self._queue_add_func(self._hub_disconnected),
        )

        # Configure the window
        self.title("Program control for Lego Robot Inventor/SPIKE Prime")
        self.geometry("1000x500")
        self.minsize(600, 300)
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(0, self._update_interface)

        # Create the necessary widgets and configure it
        self._terminal = Terminal(self)
        self._hub_status = HubStatus(self)
        self._program_control = ProgramControl(self)

        self._hub_status.set_hub_state("disconnected")
        self._program_control.disable_all()

        self._program_control.play.configure(command=self._play)
        self._program_control.stop.configure(command=self._stop)
        self._program_control.upload.configure(command=self._upload)

        # Pack the widgets and start searching the hub
        self._program_control.pack(side="top", anchor="nw")
        self._hub_status.pack(side="bottom", anchor="nw")
        self._terminal.pack(fill="both", expand=True)

        threading.Thread(target=self._search_hub, daemon=True).start()

    def _update_interface(self):
        """This function modifies the interface based on the elements added to the queue."""

        while self._interface_queue.qsize():
            func: Callable = self._interface_queue.get()
            func()
        self.after_id = self.after(10, self._update_interface)

    def _filter_messages(self, jsonrpc_response: dict):
        """This function is used by the 'JSONRPC' class to filter the various received messages that are not responses.

        Args:
            jsonrpc_response (dict): The JSONRPC message provided by the 'JSONRPC' class.
        """

        # Check if it's a dictionary (JSON-RPC message). If not, the most likely scenario
        # is that it's a MicroPython string,an integer, or a float.
        # If it's none of these, it's a truncated JSON-RPC message.
        if not isinstance(jsonrpc_response, dict):
            self._queue_add_func(self._terminal.log, str(jsonrpc_response), "log")

        elif "m" in jsonrpc_response:
            response_id: str | None = None
            method = jsonrpc_response["m"]
            params = jsonrpc_response["p"]

            if "i" in jsonrpc_response:
                response_id = jsonrpc_response["i"]

            if method == "userProgram.print":
                value = str(base64.b64decode(params["value"]), "utf-8")
                self._queue_add_func(self._terminal.log, value, "log")

                if response_id:
                    self._queue_add_func(
                        async_handler(self._rpc.send_confirmation, response_id)
                    )

            elif method == "user_program_error":
                value = str(base64.b64decode(params[3]), "utf-8")
                self._queue_add_func(self._terminal.log, value, "error")

            elif method == "user_runtime_error":
                value = str(base64.b64decode(params[3]), "utf-8")
                self._queue_add_func(self._terminal.log, value, "error")

            elif method == 2:
                self._queue_add_func(self._hub_status.battery.set_percent, params[1])

    def _queue_add_func(self, func: Callable, *args, **kwargs) -> None:
        """Adds a function to the queue, primarily for making interface modifications from another thread.

        Args:
            func (Callable): The function to be called, along with its potential args or kwargs.
        """

        def _wrapper():
            func(*args, **kwargs)

        self._interface_queue.put(_wrapper)

    def _connect_to_hub(self, port: str):
        """Function called by the 'search_hub' function when it finds a hub to connect to
        and start receiving data.

        Args:
            port (str): The port to which the hub is connected.
        """

        self._ser = serial.Serial(port)
        self._rpc.connect(self._ser)
        threading.Thread(target=self._rpc.receive_forever, daemon=True).start()

        # Configure the interface
        self._set_hub_version()
        self._program_control.active_all()

    def _hub_disconnected(self):
        """Function called by the 'JSONRPC' class when it detects that the hub has been disconnected."""

        self._hub_status.set_hub_state("disconnected")
        self._program_control.disable_all()

        threading.Thread(target=self._search_hub, daemon=True).start()

    def _on_close(self):
        for after_id in self.tk.eval("after info").split():
            self.after_cancel(after_id)
        self.destroy()

    def _search_hub(self):
        """Function to search for a Mindstorms or SPIKE Prime hub based on their vid and pid."""

        found = True
        while found:
            for device in serial.tools.list_ports.comports():
                time.sleep(0.5)
                if device.vid == 0x0694 and device.pid in [0x0008, 0x0010]:
                    self._queue_add_func(self._connect_to_hub, device.device)
                    found = False

    @async_handler
    async def _play(self):
        self._terminal.clear()

        slot = self._program_control.program_chooser.slot
        await self._rpc.play_program(slot)

    @async_handler
    async def _stop(self):
        await self._rpc.stop_program()

    @async_handler
    async def _set_hub_version(self):
        response = await self._rpc.get_hub_info()

        runtime_version = ".".join(str(nb) for nb in response["runtime"]["version"])
        firmware_version = ".".join(str(nb) for nb in response["firmware"]["version"])

        self._hub_status.set_hub_state(
            "connected", runtime=runtime_version, firmware=firmware_version
        )

    @async_handler
    async def _upload(self):
        # Adding these two lines at the beginning of the file allows
        # replacing standard prints with Lego's JSONRPC.
        print_override = textwrap.dedent(
            """\
            from util.print_override import spikeprint
            print = spikeprint
        """
        )

        file = self._program_control.upload_file
        if file:
            self._program_control.upload.configure(state="disabled")
            with open(file, "rb") as python_file:
                raw_data = python_file.read()

            with StringIO() as python_data:
                python_data.write(print_override)
                python_data.write(raw_data.decode("utf-8"))
                python_data.seek(0)

                proc, mpy = mpy_cross_v5.mpy_cross_compile(
                    "__init__.py", python_data.read()
                )

            # Get all information for the transfer requests
            actual_time = int(time.time() * 1000)
            slot = self._program_control.upload_chooser.slot
            project_name = file.stem
            size = len(mpy) if proc.returncode == 0 and mpy else len(raw_data)
            file_name = "__init__.mpy" if proc.returncode == 0 else "__init__.py"

            prog_start = await self._rpc.start_write_program(
                project_name,
                size,
                slot,
                actual_time,
                actual_time,
                file_name,
            )
            blocksize = prog_start["blocksize"]
            transferid = prog_start["transferid"]

            # Write the data to the hub
            data_to_write = mpy if proc.returncode == 0 and mpy else raw_data

            with BytesIO(data_to_write) as byte_stream:
                for block in iter(functools.partial(byte_stream.read, blocksize), b""):
                    await self._rpc.write_package(block, transfer_id=transferid)

            self._program_control.upload.configure(state="active")
            tkm.showinfo(
                "Program uploaded", "The program has been successfully uploaded."
            )

        else:
            tkm.showerror("File error", "You must choose a file.")


def main():
    app = App()
    app.async_mainloop()


if __name__ == "__main__":
    main()
