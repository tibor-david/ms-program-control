from typing import Literal, Any
import customtkinter as ctk


class Terminal(ctk.CTkFrame):
    def __init__(self, master: Any):
        super().__init__(master)

        # Initialize the tracker to alter the text color when the appearance is modified
        tracker = ctk.AppearanceModeTracker()
        tracker.add(self._update_appearance, self)

        # Create the textbox, configure it, and then pack it
        self._text_box = ctk.CTkTextbox(self)

        self._text_box.configure(state="disabled")
        self._text_box.tag_config("log", foreground="white")
        self._text_box.tag_config("error", foreground="red")

        self._text_box.pack(fill="both", expand=True, side="left")

    def log(self, message: Any, msg_type: Literal["error", "log"] = "log") -> None:
        self._text_box.configure(state="normal")
        self._text_box.insert("end", message, msg_type)
        self._text_box.configure(state="disabled")

    def clear(self):
        self._text_box.configure(state="normal")
        self._text_box.delete("1.0", "end")
        self._text_box.configure(state="disabled")

    def _update_appearance(self, appearance: str):
        if appearance == "Light":
            self._text_box.tag_config("log", foreground="black")
        else:
            self._text_box.tag_config("log", foreground="white")
