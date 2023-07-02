import base64
import os
from packaging import version
import random
import requests
import serial
import serial.tools.list_ports
import string
import threading
import time
import tomli
import tkinter.messagebox as tkm

VERSION = "1.1.0"

from .jsonrpc import JSONRPC
from .terminal_gui import Terminal


class App:

    def __init__(self):
        self.terminal = Terminal(play=self.play_program, stop=self.stop_program, upload=self.upload_pogram)

        self.terminal.protocol("WM_DELETE_WINDOW", self.on_close)

        self.rpc = None
        self.interface_run = True
        self.get_output = True
        
        self.terminal.set_hub_state("disconnected")
        threading.Thread(target=self.search_hub, daemon=True).start()

        self.terminal.after(10, self.check_version)
        self.terminal.mainloop()

    # Function to for search a hub and connect to it
    def search_hub(self):
        found = False
        while not found and self.interface_run:
            for device in serial.tools.list_ports.comports():
                if device.vid == 0x0694 and device.pid in [0x0008, 0x0010]:
                    self.rpc = JSONRPC(device.name)
                    
                    firmware_version, runtime_version = self.get_hub_version()
                    self.terminal.set_hub_state(hubstate="connected", version=" / ".join([firmware_version, runtime_version]))

                    threading.Thread(target=self.receive_hub_output, daemon=True).start()
                    found = True
            time.sleep(0.5)
    
    # Function for receive the hub output (programs prints, errors and the battery state of the hub)
    def receive_hub_output(self):
        while self.get_output and self.interface_run:
            try:
                msg = self.rpc.receive_message()
                if  isinstance(msg, dict):
                    if "m" in msg.keys():
                        if msg["m"] == "userProgram.print":
                            self.terminal.write(base64.b64decode(msg["p"]["value"]).decode().rstrip("\n"), type="normal")
                            self.rpc.send_message({"i":msg["i"]}, False)

                        elif msg["m"] == "user_program_error":
                            self.terminal.write(base64.b64decode(msg["p"][3]).decode().rstrip("\n"), type="error")

                        elif msg["m"] == "user_runtime_error":
                            self.terminal.write(base64.b64decode(msg["p"][3]).decode("utf-8").rstrip("\n"))

                        elif msg["m"] == 2:
                            self.terminal.hub_battery.set_percent(msg["p"][1])
                else:
                    self.terminal.write(str(msg), type="normal")
            except serial.SerialException:
                self.rpc = None

                self.terminal.set_hub_state("disconnected")
                tkm.showerror("Connection error", "The hub as been deconnected")

                threading.Thread(target=self.search_hub, daemon=True).start()
                break

    # Rpc methods
    def play_program(self):
        if self.rpc:
            try:
                program_slot = int(self.terminal.prog_cntr.get_value())
                self.rpc.send_message({"m":"program_execute","p":{"slotid":program_slot}, "i":self.random_id()}, get_response=False)
            except serial.SerialException:
                self.rpc = None

                self.terminal.set_hub_state("disconnected")
                tkm.showerror("Connection error", "The hub as been deconnected")

                threading.Thread(target=self.search_hub, daemon=True).start()      
        else:
            tkm.showerror("Connection error", "You must first connect a hub")

    def stop_program(self):
        if self.rpc:
            try:
                self.rpc.send_message({"m":"program_terminate","p":{}, "i":self.random_id()}, get_response=False)
            except serial.SerialException:
                self.rpc = None

                self.terminal.set_hub_state("disconnected")
                tkm.showerror("Connection error", "The hub as been deconnected")

                threading.Thread(target=self.search_hub, daemon=True).start()   
        else:
            tkm.showerror("Connection error", "You must first connect a hub")

    def get_hub_info(self):
        return self.rpc.send_message({'m':"get_hub_info", 'p': {}, 'i': self.random_id()})
    
    def start_write_program(self, name, size, slot, created, modified):
        meta = {'created': created, 'modified': modified, 'name': str(base64.b64encode(name.encode()), "utf-8"), 'type': 'python', 'project_id': self.random_id(12)}
        return self.rpc.send_message({'m':'start_write_program', 'p': {'slotid':slot, 'size': size, 'meta': meta}, 'i': self.random_id()})
    
    def write_package(self, data, transfer_id):
        return self.rpc.send_message({'m':'write_package', 'p': {'data': str(base64.b64encode(data), 'utf-8'), 'transferid': transfer_id}, 'i': self.random_id()})
    
    def upload_pogram(self):
        def upload():
            try:
                if self.terminal.upload_file:
                    self.get_output = False
                    time.sleep(0.1)
                    file_path = self.terminal.upload_file
                    with open(file_path, "rb") as file:

                        size = os.path.getsize(file_path)
                        actual_time = int(time.time()*1000)
                        slot = int(self.terminal.upload_cntr.get_value())
                        prj_name = os.path.splitext(os.path.basename(file_path))[0]
                        
                        prog_start = self.start_write_program(prj_name, size, slot, actual_time, actual_time)

                        blocksize = prog_start["blocksize"]
                        transferid = prog_start["transferid"]

                        data = file.read(blocksize)

                        while data:
                            self.write_package(data, transferid)
                            data = file.read(blocksize)
                    tkm.showinfo("Program uploaded", "The program has been successfully uploaded")

                    self.rpc.ser.reset_input_buffer()
                    self.get_output = True
                    threading.Thread(target=self.receive_hub_output, daemon=True).start()
                else:
                    tkm.showerror("File error", "You must choose a file")
                    
            except serial.SerialException:
                self.rpc = None

                self.terminal.set_hub_state("disconnected")
                tkm.showerror("Connection error", "The hub as been deconnected")

                threading.Thread(target=self.search_hub, daemon=True).start()

        if self.rpc:
            threading.Thread(target=upload, daemon=True).start()
        else:
            tkm.showerror("Connection error", "You must first connect a hub")
        
    # Function for generating random names for JSON-RPC messages and program IDs
    def random_id(self, lenght:int=4):
        return "".join(random.sample((string.ascii_letters+string.digits), lenght))
    
    # Function to get firmware and runtime version
    def get_hub_version(self):
        hub_info = self.get_hub_info()

        firmware_version = ".".join(str(nb) for nb in hub_info["firmware"]["version"])
        runtime_version =  ".".join(str(nb) for nb in hub_info["runtime"]["version"])

        return firmware_version, runtime_version

    # This function checks if a new version is available, and if one is found, a pop-up window will appear.
    def check_version(self):
        try:
            toml_file = tomli.loads(requests.get("https://raw.githubusercontent.com/tibor-david/ms-program-control/master/pyproject.toml").text)

            if version.parse(toml_file["project"]["version"]) > version.parse(VERSION):
                tkm.showinfo("New version", "A new version of the module is available !")
        except requests.exceptions.ConnectionError:
            pass

    # Window closure
    def on_close(self):
        self.interface_run = False
        self.get_output = False
        self.terminal.destroy()

if __name__ == "__main__":
    App()
