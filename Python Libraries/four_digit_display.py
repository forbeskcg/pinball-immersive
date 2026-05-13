'''
# This library is for the Grove 4 Digit Display
# https://www.seeedstudio.com/Grove-4-Digit-Display.html
#
# This library was mostly copied from https://wiki.seeedstudio.com/Grove-4-Digit_Display
#  and was edited and extended by Andrew Merrill
#
# Version: 1.0, April 2026

#
# IMPORTANT NOTE: This chip REQUIRES 5 volts and does not work with 3.3 volts
#

###############################################################################

# Usage:

import board
from four_digit_display import FourDigitDisplay
display = FourDigitDisplay(board.GP1, board.GP0, 2)  # CLK pin, DIO pin, brightness (0..7)
display.show("CHIP")
display.show(1234)
display.show([0b0111001, 0b0001001, 0b0001001, 0b0001111])
display.clear()

# show will accept:
#   a positive integer with up to 4 digits
#   a negative integer with up to 3 digits
#   a string with up to 4 of these characters:
#           upper case letters: "ABCDEFGHIJKLOPRSUVYZ"
#           lower case letters: "bcdhlnor"
#           or underscore "_" hyphen "-" space " "
#   a list with exactly 4 integers, each of which is a 7 bit binary number 
#           each bit corresponds to one led segment:
#               bit 0: top
#               bit 1: uppper right
#               bit 2: lower right
#               bit 3: bottom
#               bit 4: lower left
#               bit 5: upper left
#               bit 6: middle

###############################################################################

# Example 1:

import board, time
from four_digit_display import FourDigitDisplay
display = FourDigitDisplay(board.GP1, board.GP0)

while True:
    now = time.localtime()
    display.show(now[4]*100 + now[5])
    display.set_colon(True)
    time.sleep(1)

###############################################################################

# Example 2:

import board, time
from four_digit_display import FourDigitDisplay
display = FourDigitDisplay(board.GP1, board.GP0)

pattern = [
    [0b0000001, 0b0000000, 0b0000000, 0b0000000],
    [0b0000000, 0b0000001, 0b0000000, 0b0000000],
    [0b0000000, 0b0000000, 0b0000001, 0b0000000],
    [0b0000000, 0b0000000, 0b0000000, 0b0000001],
    [0b0000000, 0b0000000, 0b0000000, 0b0000010],
    [0b0000000, 0b0000000, 0b0000000, 0b0000100],
    [0b0000000, 0b0000000, 0b0000000, 0b0001000],
    [0b0000000, 0b0000000, 0b0001000, 0b0000000],
    [0b0000000, 0b0001000, 0b0000000, 0b0000000],
    [0b0001000, 0b0000000, 0b0000000, 0b0000000],
    [0b0010000, 0b0000000, 0b0000000, 0b0000000],
    [0b0100000, 0b0000000, 0b0000000, 0b0000000]
    ]
    
index = 0
while True:
    display.show(pattern[index])
    index += 1
    index %= len(pattern)
    time.sleep(0.05)


###############################################################################


## License

The MIT License (MIT)

Grove Base Hat for the Raspberry Pi, used to connect grove sensors.
Copyright (C) 2018  Seeed Technology Co.,Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import time, board, digitalio

charmap = {
    '0': 0x3f,
    '1': 0x06,
    '2': 0x5b,
    '3': 0x4f,
    '4': 0x66,
    '5': 0x6d,
    '6': 0x7d,
    '7': 0x07,
    '8': 0x7f,
    '9': 0x6f,
    'A': 0x77,
    'B': 0x7f,
    'b': 0x7C,
    'C': 0x39,
    'c': 0x58,
    'D': 0x3f,
    'd': 0x5E,
    'E': 0x79,
    'F': 0x71,
    'G': 0x7d,
    'H': 0x76,
    'h': 0x74,
    'I': 0x06,
    'J': 0x1f,
    'K': 0x76,
    'L': 0x38,
    'l': 0x06,
    'n': 0x54,
    'O': 0x3f,
    'o': 0x5c,
    'P': 0x73,
    'R': 0x77,
    'r': 0x50,
    'S': 0x6d,
    'U': 0x3e,
    'V': 0x3e,
    'Y': 0x66,
    'Z': 0x5b,
    '-': 0x40,
    '_': 0x08,
    ' ': 0x00
}

ADDR_AUTO = 0x40
ADDR_FIXED = 0x44
STARTADDR = 0xC0
BRIGHT_DARKEST = 0
BRIGHT_DEFAULT = 2
BRIGHT_HIGHEST = 7

class GPIO:
    # this GPIO helper class was written by Andrew Merrill

    OUT = digitalio.Direction.OUTPUT
    IN = digitalio.Direction.INPUT

    def __init__(self, pin, direction):
        self.pin = pin
        self.gp = digitalio.DigitalInOut(pin)
        self.gp.direction = direction

    def write(self, value):
        self.gp.value = (value == 1)

    def read(self):
        return self.gp.value

    def dir(self, direction):
        self.gp.direction = direction


class FourDigitDisplay(object):
    colon_index = 1

    def __init__(self, clk, dio, brightness=BRIGHT_DEFAULT):
        self.brightness = brightness

        self.clk = GPIO(clk, direction=GPIO.OUT)
        self.dio = GPIO(dio, direction=GPIO.OUT)
        self.data = [0] * 4
        self.show_colon = False

    def clear(self):
        self.show_colon = False
        self.data = [0] * 4
        self._show()

    def show(self, data):
        if type(data) is str:
            for i, c in enumerate(data):
                if c in charmap:
                    self.data[i] = charmap[c]
                else:
                    self.data[i] = 0
                if i == self.colon_index and self.show_colon:
                    self.data[i] |= 0x80
                if i == 3:
                    break
        elif type(data) is int:
            self.data = [0, 0, 0, charmap['0']]
            if data < 0:
                negative = True
                data = -data
            else:
                negative = False
            index = 3
            while data != 0:
                self.data[index] = charmap[str(data % 10)]
                index -= 1
                if index < 0:
                    break
                data = int(data / 10)

            if negative:
                if index >= 0:
                    self.data[index] = charmap['-']
                else:
                    self.data = charmap['_'] + [charmap['9']] * 3
        elif type(data) is list:
            if len(data) == 4 and all([type(d) is int for d in data]):
                self.data = data
            else:
                raise ValueError('list must contain exactly 4 integers')
        else:
            raise ValueError('Not support {}'.format(type(data)))
        self._show()

    def _show(self):
        with self:
            self._transfer(ADDR_AUTO)

        with self:
            self._transfer(STARTADDR)
            for i in range(4):
                self._transfer(self.data[i])

        with self:
            self._transfer(0x88 + self.brightness)

    def update(self, index, value):
        if index < 0 or index > 4:
            return

        if value in charmap:
            self.data[index] = charmap[value]
        else:
            self.data[index] = 0

        if index == self.colon_index and self.show_colon:
            self.data[index] |= 0x80

        with self:
            self._transfer(ADDR_FIXED)

        with self:
            self._transfer(STARTADDR | index)
            self._transfer(self.data[index])

        with self:
            self._transfer(0x88 + self.brightness)


    def set_brightness(self, brightness):
        if brightness > 7:
            brightness = 7

        self.brightness = brightness
        self._show()

    def set_colon(self, enable):
        self.show_colon = enable
        if self.show_colon:
            self.data[self.colon_index] |= 0x80
        else:
            self.data[self.colon_index] &= 0x7F
        self._show()




    def _transfer(self, data):
        for _ in range(8):
            self.clk.write(0)
            if data & 0x01:
                self.dio.write(1)
            else:
                self.dio.write(0)
            data >>= 1
            time.sleep(0.000001)
            self.clk.write(1)
            time.sleep(0.000001)

        self.clk.write(0)
        self.dio.write(1)
        self.clk.write(1)
        self.dio.dir(GPIO.IN)

        while self.dio.read():
            time.sleep(0.001)
            if self.dio.read():
                self.dio.dir(GPIO.OUT)
                self.dio.write(0)
                self.dio.dir(GPIO.IN)
        self.dio.dir(GPIO.OUT)

    def _start(self):
        self.clk.write(1)
        self.dio.write(1)
        self.dio.write(0)
        self.clk.write(0)

    def _stop(self):
        self.clk.write(0)
        self.dio.write(0)
        self.clk.write(1)
        self.dio.write(1)

    def __enter__(self):
        self._start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop()
