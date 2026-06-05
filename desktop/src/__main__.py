import threading
import lib.datalink_server as datalink_server
import queue
import lib.graphics as graphics


def startWorld(world):
    world.sounds = {
        "winner_bell": graphics.loadMusic("./desktop/sounds/winner_bell.mp3"),
        "winning_slots": graphics.loadMusic("./desktop/sounds/winning_slots.mp3"),
        "slots": graphics.loadMusic("./desktop/sounds/slots.mp3"),
        "roulette_spin": graphics.loadMusic("./desktop/sounds/roulette_spin.mp3"),
        "kids_cheering": graphics.loadMusic("./desktop/sounds/kids_cheering.mp3"),
        "lose_tone": graphics.loadMusic("./desktop/sounds/lose_tone.mp3"),
    }


def updateWorld(world):
    task = queue.get()

    if task is None:
        return

    print(f"task: {task}")

    if task[0] == "music":
        # DO NOT remove or change existing sounds
        if task[1] == 1:
            graphics.playMusic(world.sounds["winner_bell"])


if __name__ == "__main__":
    queue = queue.SimpleQueue()

    link = threading.Thread(target=lambda: datalink_server.run(queue))
    link.daemon = True
    link.start()

    graphics.makeGraphicsWindow(1920, 1080)
    graphics.runGraphics(startWorld, updateWorld, lambda world: ...)
