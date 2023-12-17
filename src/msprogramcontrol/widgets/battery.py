import pathlib
import customtkinter as ctk
from PIL import Image, ImageTk
from typing import Any


class Battery(ctk.CTkFrame):
    def __init__(self, master: Any = None):
        super().__init__(master)

        self._master = master
        self.after(0, self.update_appearance, ctk.get_appearance_mode())

        # Initialize the tracker to alter the canvas background when the appearance is modified
        tracker = ctk.AppearanceModeTracker()
        tracker.add(self.update_appearance, self)

        # Create all elements of the canvas
        self._battery_level = ctk.CTkCanvas(
            self, width=30, height=15, bd=0, highlightthickness=0
        )
        self._border_img_light = ImageTk.PhotoImage(
            Image.open(self._resource_path("./../assets/battery-light.png"))
        )
        self._border_img_dark = ImageTk.PhotoImage(
            Image.open(self._resource_path("./../assets/battery-dark.png"))
        )

        self._border = self._battery_level.create_image(0, 0, anchor="nw")
        self._battery_level_indicator = self._battery_level.create_rectangle(
            2, 2, 0, 12, state="hidden"  # type:ignore
        )

        # Create the percent label
        self._battery_level_percent = ctk.CTkLabel(self, text="N/A")

        # Pack the widgets
        self._battery_level.pack(side="left", padx=1)
        self._battery_level_percent.pack(side="right", padx=1)

    def update_appearance(self, appearance: str):
        # Configure the battery border
        if appearance == "Light":
            img = self._border_img_dark

        else:
            img = self._border_img_light

        # Configure the battery background
        if self._fg_color != "transparent":
            light_color, dark_color = self._master._fg_color
        else:
            light_color, dark_color = self._detect_color_of_master()
        bg = light_color if appearance == "Light" else dark_color

        # Edit widgets with current values
        self._battery_level.itemconfig(self._border, image=img)
        self._battery_level.config(bg=bg)

    def set_percent(self, percent: int) -> None:
        color = "red"

        if 0 <= percent <= 20:
            color = "red"
        elif percent <= 40:
            color = "orange"
        elif percent <= 100:
            color = "green"
        else:
            raise ValueError(
                f"You must provide a value between 0 and 100, not {percent}."
            )

        size = percent * 24 / 100 if percent > 3 else 0.5
        self._battery_level.itemconfigure(
            self._battery_level_indicator,
            state="normal" if percent != 0 else "hidden",
            fill=color,
            outline=color,
        )

        self._battery_level.coords(self._battery_level_indicator, 2, 2, size, 12)
        self._battery_level_percent.configure(text=f"{percent}%")

    def _resource_path(self, relative_path: str) -> pathlib.Path:
        return pathlib.Path(__file__).resolve().parent / relative_path
