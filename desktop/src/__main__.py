import threading
import lib.datalink_server as datalink_server
import queue
import lib.graphics as graphics


def hello_world() -> None:
    print("Hello World!")


def play_sound(sound: int) -> None:
    if sound == 1:
        winner_bell = graphics.loadSound("./sounds/winner bell.mp3")
        winner_bell.play()


if __name__ == "__main__":
    queue = queue.SimpleQueue()

    play_sound(1)

    link = threading.Thread(target=lambda: datalink_server.run(queue))
    link.daemon = True
    link.start()

    while True:
        task = queue.get()

        if task is None:
            continue

        print(f"task: {task}")

        if task[0] == "music":
            play_sound(task[1])
