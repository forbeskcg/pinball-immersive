# Four Digit Display

    * Download the [four_digit_display.py](libraries/four_digit_display.py) library (read library for more documentation and examples)
    * Import the libraries:
        * `import board`
        * `from four_digit_display import FourDigitDisplay`
    * Initialize with CLK pin, DIO pin, and optionally brightness (0..7)
        * `display = FourDigitDisplay(board.GP1, board.GP0, 2)`
    * To display an integer:
        * `display.show(1540)`
    * To display a string (up to four characters, only certain letters supported):
        * `display.show("LOSE")`
    * To control the individual LED segments directly:
        * `display.show([0b0111001, 0b0001001, 0b0001001, 0b0001111])`
    * To enable to colon between the second and third digit:
        * `display.set_colon(True)`
    * To change the brightness:
        * `display.set_brightness(7)`
    * To clear the display:
        * `display.clear()`
