import threading
import time
import lib.datalink_server as datalink_server
import queue


def hello_world() -> None:
    print("Hello World!")


if __name__ == "__main__":
    queue = queue.SimpleQueue()

    t = threading.Thread(target=hello_world)
    t.daemon = True
    t.start()
    link = threading.Thread(target=lambda: datalink_server.run(queue))
    link.daemon = True
    link.start()
    while True:
        time.sleep(5)
