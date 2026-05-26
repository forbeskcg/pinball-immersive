# Programming for Pinball

??? note "Getting Started"

    * We will be using Python to program the control boards for our pinball machines.
    * When you attach a board to your laptop via a USB cable, it will show up as an external drive called CIRCUITPY
    * The drive should contain a file called **`code.py`** that will be executed automatically when the board is powered on.
    * Your program should contain some initialization instructions, and then a `while True:` loop that will run forever while the board is powered on.
    * Editors
        * We recommend using the [Mu Editor](https://codewith.mu) to program the boards in Python.
        * You can also try the [CircuitPython Code Editor](https://code.circuitpython.org) which is a web-based editor (nothing to install on your computer).


??? note "Digital Input: Polling"

    Polling a Digital Input will tell if an input is on at the moment, but might miss or double-count events.

    * Import pre-installed libraries:
        * `import board, digitalio`
    * `Attach to one of the General Purpose Input/Output (GP) pins (GP0, GP1, ...):
        * `button1 = digitalio.DigitalInOut(board.GP0)`
    * Enable input mode, and either specify Pull Up or Pull Down:
        * `button1.switch_to_input(pull=digitalio.Pull.UP)` 
        * `button1.switch_to_input(pull=digitalio.Pull.DOWN)`
    * You can alternatively set input mode manually:
        *  `button1.direction = digitalio.Direction.INPUT`
    * You can also set the Pull direction manually:
        * `button1.pull = digitalio.Pull.UP`
        * `button1.pull = digitalio.Pull.DOWN`
    * You can check the current state of the input:
        * `if button1.value == True:`
        * `if button1.value == False:    # good choice for Pulled Up input buttons`
    * See reference documentation for the [digitalio](https://docs.circuitpython.org/en/latest/shared-bindings/digitalio) library


??? note "Digital Input: Listening"

    Listening to a Digital Input will tell you about every time a digital input goes on (and off) exactly once, even if it happened while you were busy doing something else.

    * Import pre-installed libraries:
        * `import board, keypad`
    * Configure the inputs to listen to:
        * `input = keypad.Keys([board.GP4, board.GP5], value_when_pressed=False)`
        * First argument is a list of GP pins to listen to
        * Second argument is a boolean, True if inputs read high when pressed, False if inputs read low (grounded) when pressed.  All inputs must be configured the same way.
    * Listen for inputs:
        ```
        while input.events:
            event = input.events.get()
            if event.key_number == 0 and event.pressed:
                # key 0 (GP4 in this example) was pressed, do something
            if event.key_number == 1 and event.released:
                # key 1 (GP5 in this example) was released, do something```
    * See reference documentation for the [keypad](https://docs.circuitpython.org/en/latest/shared-bindings/keypad) library
    * Some things to note:
        * When `value_when_pressed=False`:
            * Sensors will detect something moving into view using `event.pressed`
            * Switches with the wire connected to NC (normally closed) will detect the button being pressed using `event.released` and the button being released using `event.pressed`


??? note "Digital Output"
    A Digital Output can be used to light an LED, etc.

    * Import pre-installed libraries:
        * `import board, digitalio`
    * Attach to one of the General Purpose Input/Output (GP) pins (GP0, GP1, ...):
        * `led1 = digitalio.DigitalInOut(board.GP1)`
    * Enable input mode, and specify the initial value to output:
        * `led1.switch_to_output(value=True)`
        * `led1.switch_to_output(value=False)`
    * You can alternatively set output mode manually:
        * `led1.direction = digitalio.Direction.OUTPUT`
    * You can set the value of the output:
        * `led1.value = True`
        * `led1.value = False`
    * See reference documentation for the [digitalio](https://docs.circuitpython.org/en/latest/shared-bindings/digitalio) library

