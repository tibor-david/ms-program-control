import logging
import base64
import serial
import json


class JSONRPC:
    def __init__(self, port, debug=False):
        self.ser = serial.Serial(port, baudrate=115200)

        if debug:
            logging.basicConfig(level=logging.DEBUG)

    def receive_message(self):
        receive_buf = bytearray()

        while True:
            pos = receive_buf.find(b"\x0d")
            if pos >= 0:
                result = receive_buf[:pos]
                receive_buf = receive_buf[pos + 1 :]
                try:
                    return json.loads(result.decode("utf-8"))
                except json.JSONDecodeError:
                    logging.debug(f"Cannot parse : {result}")
            receive_buf += self.ser.read()

    def send_message(self, msg: dict, get_response: bool = True):
        msg_string = json.dumps(msg)
        logging.debug(f"Sending : {msg_string}")
        self.ser.write(msg_string.encode("utf-8") + b"\x0D")

        if get_response:
            return self.receive_response(msg["i"])

    def receive_response(self, id: str):
        while True:
            message = self.receive_message()
            if "i" in message and message["i"] == id:
                logging.debug(f"Receive response : {message}")
                if "e" in message:
                    error = json.loads(base64.b64decode(message["e"]).decode("utf-8"))
                    raise ConnectionError(error)
                return message["r"]
            logging.debug(f"While waiting for response {message}")
