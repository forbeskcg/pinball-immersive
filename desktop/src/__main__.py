import threading
import lib.datalink_server as datalink_server
import queue
import lib.graphics as graphics


def startWorld(world):
    world.sounds.winner_bell = graphics.loadSound("./sounds/winner bell.mp3")


def updateWorld(world):
    task = queue.get()

    if task is None:
        return

    print(f"task: {task}")

    if task[0] == "music":
        if task[1] == 1:
            world.sounds.winner_bell.play()


if __name__ == "__main__":
    queue = queue.SimpleQueue()

    link = threading.Thread(target=lambda: datalink_server.run(queue))
    link.daemon = True
    link.start()

    graphics.runGraphics(startWorld, updateWorld, lambda world: ...)
