import customtkinter as ctk
import pathlib
from typing import Any
from PIL import Image


class SlotChooser(ctk.CTkFrame):
    def __init__(self, master: Any | None = None):
        super().__init__(master)
        self._slot = 0

        # Create the arrows
        self._left_arrow_img = ctk.CTkImage(
            Image.open(self._resource_path("./../assets/caret-left.png")),
            size=(15, 15),
        )
        self._left_arrow = ctk.CTkButton(
            self,
            image=self._left_arrow_img,
            width=15,
            height=50,
            text="",
            command=self._decrement_count,
        )

        self._right_arrow_img = ctk.CTkImage(
            Image.open(self._resource_path("./../assets/caret-right.png")),
            size=(15, 15),
        )
        self._right_arrow = ctk.CTkButton(
            self,
            image=self._right_arrow_img,
            width=15,
            height=50,
            text="",
            command=self._increment_count,
        )

        # Create the counter label
        self._counter = ctk.CTkLabel(self, width=30, text="0", font=(None, 20, "bold"))

        # Pack the widgets
        self._left_arrow.pack(side="left")
        self._right_arrow.pack(side="right")
        self._counter.pack(fill="both", expand=True)

    @property
    def slot(self):
        return self._slot

    def _increment_count(self) -> None:
        if self._slot < 19:
            self._slot += 1
        else:
            self._slot = 0
        self._counter.configure(text=str(self._slot))

    def _decrement_count(self) -> None:
        if self._slot > 0:
            self._slot -= 1
        else:
            self._slot = 19
        self._counter.configure(text=str(self._slot))

    def _resource_path(self, relative_path: str) -> pathlib.Path:
        return pathlib.Path(__file__).resolve().parent / relative_path
