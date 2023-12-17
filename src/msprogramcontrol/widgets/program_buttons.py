import customtkinter as ctk
from tkinter import filedialog
import pathlib
from typing import Any
from .slot_chooser import SlotChooser
from PIL import Image


class ProgramButtons(ctk.CTkFrame):
    def __init__(self, master: Any | None = None) -> None:
        super().__init__(master)

        self._upload_file = None

        # Create the control buttons
        self._control_buttons = ctk.CTkFrame(self)

        self._play_img = ctk.CTkImage(
            Image.open(self._resource_path("./../assets/play.png")),
            size=(30, 30),
        )
        self.play = ctk.CTkButton(
            self, image=self._play_img, text="", width=50, height=50
        )

        self._stop_img = ctk.CTkImage(
            Image.open(self._resource_path("./../assets/stop.png")),
            size=(30, 30),
        )
        self.stop = ctk.CTkButton(
            self, image=self._stop_img, text="", width=50, height=50
        )

        self._upload_img = ctk.CTkImage(
            Image.open(self._resource_path("./../assets/download.png")),
            size=(30, 30),
        )
        self.upload = ctk.CTkButton(
            self, image=self._upload_img, text="", width=50, height=50
        )

        # Create the separation line between program launch/stop and upload section
        self._line_img = ctk.CTkImage(
            Image.open(self._resource_path("./../assets/vertical-line.png")),
            size=(25, 50),
        )
        self._line = ctk.CTkLabel(
            self, image=self._line_img, text="", height=50, width=25
        )

        # Create the SlotChooser
        self.program_chooser = SlotChooser(self)
        self.upload_chooser = SlotChooser(self)

        # Create file selection for download
        self._file_selection = ctk.CTkFrame(self)

        self._selected_file = ctk.CTkLabel(
            self._file_selection,
            text="No file chosen",
        )
        self._choose_file_btn = ctk.CTkButton(
            self._file_selection,
            text="Choose a file",
            command=self._choose_file,
        )

        # Pack the widgets
        self.play.pack(side="left", padx=5, pady=2)
        self.stop.pack(side="left", padx=5, pady=2)
        self.program_chooser.pack(side="left", padx=5, pady=2)

        self._line.pack(side="left", padx=5, pady=2)

        self.upload.pack(side="left", padx=5, pady=2)
        self._file_selection.pack(side="left", pady=2)
        self._selected_file.pack(side="top", anchor="center", padx=5)
        self._choose_file_btn.pack(side="bottom", anchor="center", padx=5)

        self.upload_chooser.pack(side="left", padx=5, pady=2)

    @property
    def upload_file(self):
        return self._upload_file

    def disable_all(self):
        self.play.configure(state="disabled")
        self.stop.configure(state="disabled")
        self.upload.configure(state="disabled")

    def active_all(self):
        self.play.configure(state="active")
        self.stop.configure(state="active")
        self.upload.configure(state="active")

    def _choose_file(self):
        file = filedialog.askopenfile(filetypes=[("Python file", "*.py")])
        if file:
            self._upload_file = pathlib.Path(file.name)

            self._choose_file_btn.configure(text="Choose another file")
            self._selected_file.configure(text=pathlib.Path(file.name).name.lower())

    def _resource_path(self, relative_path: str) -> pathlib.Path:
        return pathlib.Path(__file__).resolve().parent / relative_path
