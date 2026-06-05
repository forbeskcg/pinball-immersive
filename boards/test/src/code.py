from datalink import Datalink
from fastinput import FastInput
import board, music

datalink = Datalink(255)
input1 = FastInput(board.GP21)

while True:
    if input1.wasPressed():
        datalink.send(0, "sound", 1)

    if datalink.hasPacket():
        packet = datalink.getPacket()
