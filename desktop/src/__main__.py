import threading
import lib.datalink_server as datalink_server
import queue
import lib.graphics as graphics


def startWorld(world):
    world.sounds = [
        graphics.loadMusic("./desktop/sounds/winner_bell.mp3"),
        graphics.loadMusic("./desktop/sounds/winning_slots.mp3"),
        graphics.loadMusic("./desktop/sounds/slots.mp3"),
        graphics.loadMusic("./desktop/sounds/roulette_spin.mp3"),
        graphics.loadMusic("./desktop/sounds/kids_cheering.mp3"),
        graphics.loadMusic("./desktop/sounds/lose_tone.mp3"),
    ]


def updateWorld(world):
    task = queue.get()

    if task is None:
        return

    print(f"task: {task}")

    if task[0] == "sound":
        graphics.playMusic(world.sounds[task[1]])


if __name__ == "__main__":
    queue = queue.SimpleQueue()

    link = threading.Thread(target=lambda: datalink_server.run(queue))
    link.daemon = True
    link.start()

    graphics.makeGraphicsWindow(1920, 1080)
    graphics.runGraphics(startWorld, updateWorld, lambda world: ...)
