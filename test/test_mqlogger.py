from threading import Thread
from cuiplotlib.logging import MQLogger, mqlog, mqrecv


Thread(target=lambda: mqrecv("tcp://localhost:51840"), daemon=True).start()


# logger = MQLogger("tcp://*:51840")

while True:
    text = input()
    # logger.print(f"Received: {text}")
    mqlog(f"Received: {text}")
