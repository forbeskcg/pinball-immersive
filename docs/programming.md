# Programming for Pinball

??? note "Getting Started"


    * We will be using Python to program the control boards for our pinball machines.
    * When you attach a board to your laptop via a USB cable, it will show up as an external drive called CIRCUITPY
    * The drive should contain a file called **`code.py`** that will be executed automatically when the board is powered on.
    * Your program should contain some initialization instructions, and then a `while True:` loop that will run forever while the board is powered on.
    * Editors
        * We recommend using the [Mu Editor](https://codewith.mu) to program the boards in Python.
        * You can also try the [CircuitPython Code Editor](https://code.circuitpython.org) which is a web-based editor (nothing to install on your computer).


??? note "Digital Outputs"

    A Digital Output can be used to light an LED, etc.

    * Import pre-installed libraries:
        * `import board, digitalio`
    * Attach to one of the General Purpose Input/Output (GP) pins (GP0, GP1, ...):
        * `led1 = digitalio.DigitalInOut(board.GP1)`
    * Set the pin to output mode:
        * `led1.direction = digitalio.Direction.OUTPUT`
    * You can set the value of the output:
        * `led1.value = True`
        * `led1.value = False`
    * See reference documentation for the [digitalio](https://docs.circuitpython.org/en/latest/shared-bindings/digitalio) library

??? note "Example Program"

    ```
    import board, digitalio, time
    led1 = digitalio.DigitalInOut(board.GP1)
    led1.direction = digitalio.Direction.OUTPUT

    led1.value = True

    while True:
        time.sleep(0.1)
    ```
        
