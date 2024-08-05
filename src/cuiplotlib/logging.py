import zmq


global_logger = None


class MQLogger:
    def __init__(self, mqspec: str):
        self._socket: zmq.Socket = zmq.Context().socket(zmq.PUB)
        self._socket.bind(mqspec)

    def print(self, message: str):
        self._socket.send_string(str(message), zmq.DONTWAIT)


def mqrecv(mqspec: str = "tcp://localhost:51840"):
    socket = zmq.Context().socket(zmq.SUB)
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    socket.connect(mqspec)
    while True:
        data = socket.recv_string()
        print(data)


def mqlog(msg, mqspec: str = "tcp://*:51840"):
    global global_logger
    if global_logger is None:
        global_logger = MQLogger(mqspec)
    global_logger.print(msg)
