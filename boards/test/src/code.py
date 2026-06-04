from datalink import Datalink
from fastinput import FastInput
import board, music

datalink = Datalink(255)
input1 = FastInput(board.GP21)

while True:
    if input1.wasPressed():
        music.playTone(board.GP22, 440, 0.25, 50)
