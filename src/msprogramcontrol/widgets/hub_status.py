# import tkinter
import customtkinter as ctk
from typing import Literal, Any
import pathlib
from PIL import Image
from .battery import Battery


class HubStatus(ctk.CTkFrame):
    def __init__(self, master: Any | None = None):
        super().__init__(master)

        # Create a label to display the hub's status and configure its images
        self._red_dot = ctk.CTkImage(
            Image.open(self._resource_path("./../assets/red-circle.png")),
            size=(15, 15),
        )
        self._green_dot = ctk.CTkImage(
            Image.open(self._resource_path("./../assets/green-circle.png")),
            size=(15, 15),
        )
        self._status = ctk.CTkLabel(self, text="", image=self._red_dot)

        # Create the battery and the version label
        self.battery = Battery(self)
        self.battery.configure(fg_color="transparent")
        self._version = ctk.CTkLabel(self, text="N/A")

        # Pack the widgets
        self._status.pack(side="left")
        self._version.pack(side="left", padx=2)
        self.battery.pack(side="left", padx=2)

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
        return pathlib.Path(__file__).resolve().parent / relative_path
