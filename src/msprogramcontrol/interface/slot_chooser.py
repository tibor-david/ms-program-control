import tkinter
import pathlib


class SlotChooser(tkinter.Frame):
    def __init__(self, master: tkinter.Misc | None = None):
        super().__init__(master)
        self._slot = 0

        # Create the arrows
        self._left_arrow_img = tkinter.PhotoImage(
            file=self._resource_path("./../assets/left_arrow.png")
        )
        self._left_arrow = tkinter.Button(
            self, image=self._left_arrow_img, bd=0, command=self._decrement_count
        )

        self._right_arrow_img = tkinter.PhotoImage(
            file=self._resource_path("./../assets/right_arrow.png")
        )
        self._right_arrow = tkinter.Button(
            self, image=self._right_arrow_img, bd=0, command=self._increment_count
        )

        # Create the counter label
        self._counter = tkinter.Label(
            self, width=2, text="0", font=("tkinterDefaultFont", 20, "bold")
        )

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
        return pathlib.Path(__file__).parent / relative_path
