'''
Library for reading a fast momentary digital input using PIO

Authors: Kevin Forbes and Andrew Merrill
Version: 1.1

Example usage:

import time
from fastinput import FastInput
input1 = FastInput(board.GP5)

while True:
    if input1.wasPressed():
        # do something
        time.sleep(0.1)
        input1.reset()
'''

import adafruit_pioasm
import rp2pio
import array

fastinput_code = """
.program fastinput

loop:
    pull            ; Pull 1 word (32 bits) from the TX FIFO to the Output Shift Register (OSR)
                    ; We don't look at the contents - any data means reset

    wait 1 pin 0    ; Wait until pin 0 goes high (off)
    wait 0 pin 0    ; Wait until pin 0 goes low  (on)

    set x, 1        ; Write 1 to Register X
    in x, 1         ; Shift 1 bit from Register X to Input Shift Register (ISR)
    push            ; Push the Input Shift Register (ISR) to the RX FIFO and clear ISR
    jmp loop        ; Restart the loop
"""

fastinput_assembled = adafruit_pioasm.assemble(fastinput_code)

class FastInput:

    def __init__(self, pin):
        self.state_machine = rp2pio.StateMachine(
            fastinput_assembled,
            first_in_pin=pin,
            frequency=125000000,
            wait_for_txstall=False)

        self.output = array.array("b", [0])
        self._reset_state_machine()

    def reset(self):
        if self.state_machine.in_waiting:
            self.state_machine.clear_rxfifo()
            self._reset_state_machine()

    def _reset_state_machine(self):
        self.state_machine.write(self.output)

    # returns true if the input pin was set (low) since the last time that wasPressed() was called
    def wasPressed(self):
        if self.state_machine.in_waiting:
            self.state_machine.clear_rxfifo()
            self._reset_state_machine()
            return True
        else:
            return False

