import threading
import time


def hello_world() -> None:
    print("Hello World!")


if __name__ == "__main__":
    t = threading.Thread(target=hello_world)
    t.daemon = True
    t.start()
    while True:
        time.sleep(5)
