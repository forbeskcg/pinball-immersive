import threading
import lib.datalink_server as datalink_server
import queue
import graphics


def hello_world() -> None:
    print("Hello World!")


def play_sound(sound: int) -> None:
    if sound == 1:
        winner_bell = graphics.loadSound("./sounds/winner bell.mp3")
        winner_bell.play()


if __name__ == "__main__":
    queue = queue.SimpleQueue()

    link = threading.Thread(target=lambda: datalink_server.run(queue))
    link.daemon = True
    link.start()

    while True:
        task = queue.get()

        if task is None:
            continue

        if task[0] == "music":
            play_sound(task[1])
