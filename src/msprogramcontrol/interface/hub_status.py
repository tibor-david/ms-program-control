import tkinter
from typing import Literal
import pathlib

from . import Battery


class HubStatus(tkinter.Frame):
    def __init__(self, master: tkinter.Misc | None = None):
        super().__init__(master)

        # Create a label to display the hub's status
        self._red_dot = tkinter.PhotoImage(
            file=self._resource_path("./../assets/red_dot.png")
        )
        self._green_dot = tkinter.PhotoImage(
            file=self._resource_path("./../assets/green_dot.png")
        )
        self._status = tkinter.Label(self)

        # Create the battery and the version label
        self.battery = Battery(self)
        self._version = tkinter.Label(self, bd=0)

        # Pack the widget
        self._status.pack()

    def _hide_all_wigdets(self):
        for widget in self.winfo_children():
            widget.pack_forget()

    def set_hub_state(
        self,
        state: Literal["connected", "disconnected"],
        firmware: str | None = None,
        runtime: str | None = None,
    ):
        if state not in ["connected", "disconnected"]:
            raise ValueError(
                "Invalid state, the state must be 'connected' or 'disconnected'."
            )

        if state == "connected":
            if not (runtime and firmware):
                raise ValueError(
                    "You must provide the firmware and the filesystem version."
                )

            self._status.configure(image=self._green_dot)
            self._version.configure(text=f"{firmware}/{runtime}")

            self._hide_all_wigdets()
            self._status.pack(side="left")
            self._version.pack(side="left", padx=2)
            self.battery.pack(side="left", padx=2)

        elif state == "disconnected":
            self._status.configure(image=self._red_dot)

            self._hide_all_wigdets()
            self._status.pack(side="left")

    def _resource_path(self, relative_path: str) -> pathlib.Path:
        return pathlib.Path(__file__).parent / relative_path
