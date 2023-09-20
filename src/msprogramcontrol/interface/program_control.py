import tkinter
from tkinter import ttk
from tkinter import filedialog
import pathlib

from .slot_chooser import SlotChooser


class ProgramControl(tkinter.Frame):
    def __init__(self, master: tkinter.Misc | None = None) -> None:
        super().__init__(master)

        self._upload_file = None

        # Create the control buttons
        self._control_buttons = tkinter.Frame()

        self._play_img = tkinter.PhotoImage(
            file=self._resource_path("./../assets/play.png")
        )
        self.play = tkinter.Button(self, image=self._play_img, bd=0)
        self._stop_img = tkinter.PhotoImage(
            file=self._resource_path("./../assets/stop.png")
        )
        self.stop = tkinter.Button(self, image=self._stop_img, bd=0)

        self._upload_img = tkinter.PhotoImage(
            file=self._resource_path("./../assets/upload.png")
        )
        self.upload = tkinter.Button(self, image=self._upload_img, bd=0)

        # Create the separation line between program launch/stop and upload
        self._line_img = tkinter.PhotoImage(
            file=self._resource_path("./../assets/separation_line.png")
        )
        self._line = tkinter.Label(self, image=self._line_img, bd=0)

        # Create the SlotChooser
        self.program_chooser = SlotChooser(self)
        self.upload_chooser = SlotChooser(self)

        # Create file selection for download
        self._file_selection = tkinter.Frame(self)

        self._selected_file = tkinter.Label(
            self._file_selection, width=18, text="No file chosen"
        )
        self._choose_file_btn = ttk.Button(
            self._file_selection,
            width=18,
            text="Choose a file",
            command=self._choose_file,
        )

        # Pack the widgets
        self.play.pack(side="left", padx=5)
        self.stop.pack(side="left", padx=5)
        self.program_chooser.pack(side="left", padx=5)

        self._line.pack(side="left", padx=5)

        self.upload.pack(side="left", padx=5)
        self._file_selection.pack(side="left")
        self._selected_file.pack(side="top", anchor="center", padx=5)
        self._choose_file_btn.pack(side="bottom", anchor="center", padx=5)

        self.upload_chooser.pack(side="left", padx=5)

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
        return pathlib.Path(__file__).parent / relative_path
