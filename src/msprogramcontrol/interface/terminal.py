import tkinter
from typing import Literal, Any


class Terminal(tkinter.Frame):
    def __init__(self, master: tkinter.Misc | None = None) -> None:
        super().__init__(master)

        # Create the scrollbar and the text zone
        self._text_zone = tkinter.Text(self)
        self._scrollbar = tkinter.Scrollbar(self)

        self._scrollbar.configure(command=self._text_zone.yview)

        self._text_zone.configure(yscrollcommand=self._scrollbar.set, state="disabled")
        self._text_zone.tag_configure("log", foreground="black")
        self._text_zone.tag_configure("error", foreground="red")

        # Pack the widgets
        self._scrollbar.pack(side="right", fill="y")
        self._text_zone.pack(side="left", fill="both", expand=True)

    def log(self, message: Any, msg_type: Literal["error", "log"] = "log") -> None:
        self._text_zone.configure(state="normal")
        self._text_zone.insert(tkinter.END, message, msg_type)
        self._text_zone.configure(state="disabled")

    def clear(self):
        self._text_zone.configure(state="normal")
        self._text_zone.delete("1.0", tkinter.END)
        self._text_zone.configure(state="disabled")
