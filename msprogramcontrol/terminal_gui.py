import os
import tkinter as tk
import tkinter.filedialog as tkf


class SlotCounter(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack_propagate(False)

        self.left_arrow_img = tk.PhotoImage(file=self._resource_path("assets/left_arrow.png"))
        self.right_arrow_img = tk.PhotoImage(file=self._resource_path("assets/right_arrow.png"))

        self.left_arrow_btn = tk.Button(self, image=self.left_arrow_img, border=0, command=self._decrement_count)
        self.right_arrow_btn = tk.Button(self, image=self.right_arrow_img, border=0, command=self._increment_count)
        
        self.counter_label = tk.Label(self, text="0", font=("TkDefaultFont", 20, "bold"))

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
        if count  > 0:
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


class Terminal(tk.Frame):

    def __init__(self, master=None, functions=(None, None, None)):
        super().__init__(master)

        self.upload_file = None
        self.functions = functions
        self.master = master

        self.terminal = tk.Text(self)
        self.scrollbar = tk.Scrollbar(self)

        self.play_img = tk.PhotoImage(file=self._resource_path("assets/play.png"))
        self.stop_img = tk.PhotoImage(file=self._resource_path("assets/stop.png"))
        self.upload_img = tk.PhotoImage(file=self._resource_path("assets/upload.png"))
        self.line_img = tk.PhotoImage(file=self._resource_path("assets/separation_line.png"))

        self.play_btn = tk.Button(master=self, image=self.play_img, border=0, width=50, height=50, command=functions[0])
        self.stop_btn = tk.Button(self, image=self.stop_img, border=0, width=50, height=50, command=functions[1])
        self.prog_cntr = SlotCounter(self)
        self.line_lbl = tk.Label(self, image=self.line_img, border=0, width=10, height=50)

        self.upload_btn = tk.Button(self, image=self.upload_img, border=0, width=50, height=50, command=functions[2])
        self.file_selction_btn = tk.Button(text="Choose a file", command=self._choose_file)
        self.status_file_lbl = tk.Label(text="No file chosen")
        self.upload_cntr = SlotCounter(self) 

        self.terminal.configure(state="disabled", yscrollcommand=self.scrollbar.set)
        self.terminal.tag_configure("normal", foreground="black")
        self.terminal.tag_configure("error", foreground="red")
        self.scrollbar.configure(command=self.terminal.yview)

        self.master.bind("<Configure>", self._resize_widgets)

        self.play_btn.place(x=0, y=5)
        self.stop_btn.place(x=60, y=5)
        self.prog_cntr.place(x=120, y=5, width=55, height=50)
        self.line_lbl.place(x=185, y=5)

        self.upload_btn.place(x=205, y=5)
        self.upload_cntr.place(x=400, y=5, width=55, height=50)
        self.file_selction_btn.place(x=265, y=5, width=125, height=25)
        self.status_file_lbl.place(width=125, height=25, x=260, y=30)

    def _resize_widgets(self, event):
        window_width = self.master.winfo_width()
        window_height = self.master.winfo_height()

        scrollbar_x = window_width-16
        terminal_width = window_width-16
        widgets_height = window_height-60

        self.terminal.place(width=terminal_width, height=widgets_height, x=0, y=60)
        self.scrollbar.place(width=16, height=widgets_height, x=scrollbar_x, y=60)

    def _choose_file(self):
        file = tkf.askopenfile(filetypes=[("Python file", "*.py")])
        if file is not None:
            self.upload_file = file.name
            self.file_selction_btn.configure(text="Choose another file")
            self.status_file_lbl.configure(text=os.path.basename(self.upload_file).lower())
    
    def _resource_path(self, relative_path):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
    
    def write(self, text, type:str):
        self.terminal.configure(state="normal")
        self.terminal.insert("end", str(text)+"\n", type)
        self.terminal.see("end")
        self.terminal.configure(state="disabled")
        self.terminal.update()
