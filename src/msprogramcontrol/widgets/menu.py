import tkinter as tk
import customtkinter as ctk
from typing import Any


class Menu(tk.Menu):
    def __init__(self, master: Any):
        super().__init__(master=master)

        # Create the menu of the ms-program-control library
        self._appearance_menu = tk.Menu(self, tearoff=0)
        self._appearance = tk.StringVar(value="dark")

        self.add_cascade(label="Appearance", menu=self._appearance_menu)

        self._appearance_menu.add_radiobutton(
            label="Dark",
            variable=self._appearance,
            value="dark",
            command=self._set_appearance,
        )
        self._appearance_menu.add_radiobutton(
            label="Light",
            variable=self._appearance,
            value="light",
            command=self._set_appearance,
        )
        self._appearance_menu.add_radiobutton(
            label="System",
            variable=self._appearance,
            value="system",
            command=self._set_appearance,
        )

    def _set_appearance(self):
        selected_appearance = self._appearance.get()
        if selected_appearance != ctk.get_appearance_mode():
            ctk.set_appearance_mode(selected_appearance)
            self._appearance.set(selected_appearance)
