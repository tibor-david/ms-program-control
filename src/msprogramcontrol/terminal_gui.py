import os
import tkinter as tk
import tkinter.filedialog as tkf
from typing import Callable


class SlotCounter(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.left_arrow_img = tk.PhotoImage(
            file=self._resource_path("assets/left_arrow.png")
        )
        self.right_arrow_img = tk.PhotoImage(
            file=self._resource_path("assets/right_arrow.png")
        )

        self.left_arrow_btn = tk.Button(
            self, image=self.left_arrow_img, bd=0, command=self._decrement_count
        )
        self.right_arrow_btn = tk.Button(
            self, image=self.right_arrow_img, bd=0, command=self._increment_count
        )

        self.counter_label = tk.Label(
            self, text="0", font=("TkDefaultFont", 20, "bold"), width=2
        )

        self.left_arrow_btn.pack(side="left")
        self.right_arrow_btn.pack(side="right")

        self.counter_label.pack(fill="both", expand=True)

    def _increment_count(self):
        count = int(self.counter_label["text"])
        if count < 19:
            count += 1
            self.change_value(str(count))
        else:
            self.change_value("0")

    def _decrement_count(self):
        count = int(self.counter_label["text"])
        if count > 0:
            count -= 1
            self.change_value(str(count))
        else:
            self.change_value("19")

    def _resource_path(self, relative_path):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

    def get_value(self):
        return self.counter_label["text"]

    def change_value(self, value):
        self.counter_label.configure(text=value)


class Battery(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.battery_border_img = tk.PhotoImage(
            file=self._resource_path("assets/battery.png")
        )

        self.battery_cnvs = tk.Canvas(
            self, width=30, height=15, bd=0, highlightthickness=0
        )
        self.battery_percent_lbl = tk.Label(self, text="N/A", bd=0)

        self.battery_bar = self.battery_cnvs.create_rectangle(
            2, 2, 0, 12, state="hidden"
        )
        self.battery_border = self.battery_cnvs.create_image(
            0, 0, image=self.battery_border_img, anchor="nw"
        )

        self.battery_cnvs.pack(side="left")
        self.battery_percent_lbl.pack(side="right")

    def set_percent(self, percent: int):
        if 0 <= percent <= 100:
            if percent != 0:
                size = percent * 24 / 100
                color = "red"

                if percent <= 20:
                    color = "red"
                elif 20 < percent <= 40:
                    color = "orange"
                elif 40 < percent <= 100:
                    color = "green"

                self.battery_cnvs.itemconfigure(
                    self.battery_bar, state="normal", fill=color, outline=color
                )
                self.battery_cnvs.coords(self.battery_bar, 2, 2, size, 12)
                self.battery_percent_lbl.configure(text=str(percent) + "%")
            else:
                self.battery_cnvs.itemconfigure(self.battery_bar, state="hidden")
                self.battery_percent_lbl.configure(text="0%")

    def _resource_path(self, relative_path):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


class Terminal(tk.Tk):
    def __init__(self, play: Callable, stop: Callable, upload: Callable):
        super().__init__()

        self.upload_file = None

        self.title("Program control for Lego Robot Inventor/SPIKE Prime")
        self.geometry("1000x500")
        self.minsize(600, 300)

        # Frames
        self.terminal_frm = tk.Frame()
        self.terminal_frm.pack_propagate(False)

        self.control_btns_frm = tk.Frame()

        self.hub_status_frm = tk.Frame()

        # Terminal frame
        self.terminal_scrllbr = tk.Scrollbar(self.terminal_frm)
        self.terminal_txt = tk.Text(self.terminal_frm)

        self.terminal_txt.configure(
            yscrollcommand=self.terminal_scrllbr.set, state="disabled"
        )
        self.terminal_txt.tag_configure("normal", foreground="black")
        self.terminal_txt.tag_configure("error", foreground="red")

        self.terminal_scrllbr.configure(command=self.terminal_txt.yview)

        self.terminal_scrllbr.pack(side="right", fill="y")
        self.terminal_txt.pack(side="left", fill="both", expand=True)

        # Program buttons frame
        self.play_img = tk.PhotoImage(file=self._resource_path("assets/play.png"))
        self.stop_img = tk.PhotoImage(file=self._resource_path("assets/stop.png"))
        self.upload_img = tk.PhotoImage(file=self._resource_path("assets/upload.png"))
        self.line_img = tk.PhotoImage(
            file=self._resource_path("assets/separation_line.png")
        )

        self.play_btn = tk.Button(
            self.control_btns_frm, image=self.play_img, bd=0, command=play
        )
        self.stop_btn = tk.Button(
            self.control_btns_frm, image=self.stop_img, bd=0, command=stop
        )
        self.prog_cntr = SlotCounter(self.control_btns_frm)
        self.line_lbl = tk.Label(self.control_btns_frm, image=self.line_img, bd=0)

        self.upload_btn = tk.Button(
            self.control_btns_frm, image=self.upload_img, bd=0, command=upload
        )

        self.file_selction_frm = tk.Frame(self.control_btns_frm)
        self.file_selction_btn = tk.Button(
            self.file_selction_frm,
            text="Choose a file",
            command=self._choose_file,
            width=18,
        )
        self.status_file_lbl = tk.Label(
            self.file_selction_frm, text="No file chosen", width=18
        )
        self.upload_cntr = SlotCounter(self.control_btns_frm)

        self.play_btn.pack(side="left", padx=5)
        self.stop_btn.pack(side="left", padx=5)
        self.prog_cntr.pack(side="left", padx=5)
        self.line_lbl.pack(side="left", padx=5)

        self.upload_btn.pack(side="left", padx=5)
        self.file_selction_btn.pack(side="top", anchor="center", padx=5)
        self.status_file_lbl.pack(side="bottom", anchor="center", padx=5)
        self.file_selction_frm.pack(side="left", padx=5)
        self.upload_cntr.pack(side="left", padx=5)

        # Hub status frame
        self.green_dot_img = tk.PhotoImage(
            file=self._resource_path("assets/green_dot.png")
        )
        self.red_dot_img = tk.PhotoImage(file=self._resource_path("assets/red_dot.png"))

        self.hub_state_lbl = tk.Label(self.hub_status_frm)
        self.hub_version_lbl = tk.Label(self.hub_status_frm, bd=0)
        self.hub_battery = Battery(self.hub_status_frm)

        # Pack the frames
        self.control_btns_frm.pack(anchor="w")
        self.terminal_frm.pack(fill="both", expand=True)
        self.hub_status_frm.pack(anchor="w")

    def _choose_file(self):
        file = tkf.askopenfile(filetypes=[("Python file", "*.py")])
        if file is not None:
            self.upload_file = file.name
            self.file_selction_btn.configure(text="Choose another file")
            self.status_file_lbl.configure(
                text=os.path.basename(self.upload_file).lower()
            )

    def _resource_path(self, relative_path):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

    def write(self, text, type: str):
        self.terminal_txt.configure(state="normal")
        self.terminal_txt.insert("end", str(text) + "\n", type)
        self.terminal_txt.see("end")
        self.terminal_txt.configure(state="disabled")
        self.terminal_txt.update()

    def set_hub_state(self, hubstate: str, version: str = "N/A"):
        def hide_all_widgets():
            for widget in self.hub_status_frm.winfo_children():
                widget.pack_forget()

        if hubstate == "connected":
            if version == "N/A":
                raise ValueError("You must provide a version")

            self.hub_state_lbl.configure(image=self.green_dot_img)
            self.hub_battery.set_percent(100)
            self.hub_version_lbl.configure(text=version)

            hide_all_widgets()

            self.hub_state_lbl.pack(side="left")
            self.hub_version_lbl.pack(side="left", padx=2)
            self.hub_battery.pack(side="left", padx=2)

        elif hubstate == "disconnected":
            self.hub_state_lbl.configure(image=self.red_dot_img)

            hide_all_widgets()

            self.hub_state_lbl.pack(side="left")
