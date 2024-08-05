import zmq


DEFAULT_HOST = "localhost"
DEFAULT_PORT = 51840


class MQOut:
    def __init__(self, mqspec: str = f"tcp://*:{DEFAULT_PORT}"):
        self._buf = []
        self.reset(mqspec)

    def reset(self, mqspec: str):
        self._socket: zmq.Socket = zmq.Context().socket(zmq.PUB)
        self._socket.bind(mqspec)
        self._buf.clear()

    def write(self, message: str):
        self._buf.append(message)
        if message.endswith("\n"):
            self.flush()

    def flush(self):
        self._socket.send_string("".join(self._buf), zmq.DONTWAIT)
        self._buf.clear()


def mqrecv(mqspec: str = f"tcp://{DEFAULT_HOST}:{DEFAULT_PORT}"):
    socket = zmq.Context().socket(zmq.SUB)
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    socket.connect(mqspec)
    while True:
        data = socket.recv_string()
        print(data, end="", flush=True)
