import base64
import os
import random
import string
import threading
import time
import tkinter as tk
import tkinter.messagebox as tkm
import argparse

from .jsonrpc import JSONRPC
from .terminal_gui import Terminal


class App:
    def __init__(self, port):
        self.root = tk.Tk()
        self.terminal = Terminal(self.root, (self.play, self.stop, self.upload))

        self.root.geometry("1000x500")
        self.root.minsize(500, 250)
        self.root.title("Program control for Lego Robot Inventor/SPIKE Prime")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.rpc = JSONRPC(port)

        self.run = True
        self.run_get_output()

        self.terminal.pack(fill="both", expand=True)
        self.root.mainloop()

    def get_output(self):
        while self.run:
            msg = self.rpc.receive_message()
            if type(msg) is dict:
                if "m" in msg.keys():
                    if msg["m"] == "userProgram.print":
                        self.terminal.write(base64.b64decode(msg["p"]["value"]).decode().rstrip("\n"), type="normal")
                        self.rpc.send_message({"i":msg["i"]}, False)

                    if msg["m"] == "user_program_error":
                        self.terminal.write(base64.b64decode(msg["p"][3]).decode().rstrip("\n"), type="error")

                    if msg["m"] == "user_runtime_error":
                        self.terminal.write(base64.b64decode(msg["p"][3]).decode("utf-8").rstrip("\n"))
            else:
                self.terminal.write(str(msg), type="normal")
    
    def start_write_program(self, name, size, slot, created, modified):
        meta = {'created': created, 'modified': modified, 'name': str(base64.b64encode(name.encode()), "utf-8"), 'type': 'python', 'project_id': self.random_id(12)}
        return self.rpc.send_message({'m':'start_write_program', 'p': {'slotid':slot, 'size': size, 'meta': meta}, 'i': self.random_id()})

    def write_package(self, data, transfer_id):
        return self.rpc.send_message({'m':'write_package', 'p': {'data': str(base64.b64encode(data), 'utf-8'), 'transferid': transfer_id}, 'i': self.random_id()})

    def upload_program(self, file_path, name=None):
        with open(file_path, "rb") as file:
            size = os.path.getsize(file_path)
            actual_time = int(time.time()*1000)
            slot = int(self.terminal.upload_cntr.get_value())
            if name is not None:
                prj_name = name
            else:
                prj_name = os.path.splitext(os.path.basename(file_path))[0]
            prog_start = self.start_write_program(prj_name, size, slot, actual_time, actual_time)

            blocksize = prog_start["blocksize"]
            transferid = prog_start["transferid"]

            data = file.read(blocksize)

            while data:
                self.write_package(data, transferid)
                data = file.read(blocksize)
            tkm.showinfo("Program uploaded", "The program has been successfully uploaded")

    def random_id(self, lenght=4):
        return "".join(random.sample((string.ascii_letters+string.digits), lenght))
    
    def play(self):
        slot = int(self.terminal.prog_cntr.get_value())
        self.rpc.send_message({"m":"program_execute","p":{"slotid":slot}, "i":self.random_id()}, get_response=False)

    def stop(self):
        self.rpc.send_message({"m":"program_terminate","p":{}, "i":self.random_id()},get_response=False)

    def upload(self):
        self.stop_get_output()
        if self.terminal.upload_file is not None:
            time.sleep(0.2)
            self.upload_program(self.terminal.upload_file)
            self.run_get_output()
        else:
            tkm.showerror("Error", "You must choose a file")

    def run_get_output(self):
        self.run = True
        threading.Thread(target=self.get_output, daemon=True).start()
        self.rpc.ser.reset_input_buffer()

    def stop_get_output(self):
        self.run = False

    def on_close(self):
        self.stop_get_output()
        self.root.destroy()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="Hub device path", type=str, default="/dev/ttyACM0")
    args = parser.parse_args()
    
    if args.port:
        App(args.port)
