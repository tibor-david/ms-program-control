import tkinter
import pathlib


class Battery(tkinter.Frame):
    def __init__(self, master: tkinter.Misc | None = None):
        super().__init__(master)

        # Create all elements of the battery canvas
        self._battery_level = tkinter.Canvas(
            self, width=30, height=15, bd=0, highlightthickness=0
        )
        self._border_img = tkinter.PhotoImage(
            file=self._resource_path("./../assets/battery.png")
        )
        self._border = self._battery_level.create_image(
            0, 0, image=self._border_img, anchor="nw"
        )
        self._battery_level_indicator = self._battery_level.create_rectangle(
            2, 2, 0, 12, state="hidden"
        )

        # Create the percent label
        self._battery_level_percent = tkinter.Label(self, text="N/A", bd=0)

        # Pack the widgets
        self._battery_level.pack(side="left")
        self._battery_level_percent.pack(side="right")

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

    def _resource_path(self, relative_path) -> pathlib.Path:
        return pathlib.Path(__file__).parent / relative_path
