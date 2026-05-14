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


??? note "NeoPixel Colored LEDs"

    * Import pre-installed libraries:
        * `import board, neopixel`
    * Initialize with pin and number of attached pixels
    * For example, to control the two NeoPixels built in to our Cytron Maker Pi RP20240 board:
        * `pixels = neopixel.NeoPixel(board.GP18, 2)`
    * Use as if it were a list of (R,G,B) tuples
        * `pixels[0] = (255,0,0) # red`
        * `pixels[1] = (255,255,255)  # white`
    * Set all pixels to same color with `fill` function:
        * `pixels.fill((0,255,0)) # all set to green`
    * See reference documentation for the [neopixel](https://docs.circuitpython.org/projects/neopixel/en/latest/api.html) library

??? note "Four Digit Display"

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

??? note "Playing Tones and Notes on the Piezo Buzzer"

    * Download the [music.py](libraries/music.py) library (read library for more detailed documentation)
    * Import the libraries:
    import board, music
    * On our boards, the piezo buzzer is GP pin 22
    * Play a single tone with a given frequency (in hertz), duration (in seconds), volume (0..100):
        * `music.playTone(board.GP22, 440, 0.25, 50)`
    * Play a series of tones from the given list of frequencies, duration (in seconds), volume (0..100):
        * `music.playTones(board.GP22, [400, 500, 600], 0.25, 50)`
    * Play a single musical note, with a given letter note from 'A' to 'G', or sharp (like 'A#') or flat (like 'Ab'), and a given octave number (usually in the range 1..9), and duration (in seconds), volume (0..100):
        * `music.playNote(board.GP22, 'A', 4, 0.25, 50)`
    * Play a series of musical notes from a list, where each note in the list is a (letter, octave, duration) tuple, and volume is in the range 0..100:
        * `music.playNotes(board.GP22,[('B',4,0.25),('C',5,0.25),('G',5,0.25)],50)`

??? note "Play Music from a WAV audio file"

    * Note: You will probably need to edit/convert your WAV file before playing it.
    * We recommend using the excellent free program [Audacity](https://www.audacityteam.org) to edit/convert WAV files
    * Export your WAV file with these settings:
        * Mono channel (not stereo)
        * The encoding should be either Unsigned 8-bit PCM or Signed 16-bit PCM 
        * You might need to use a lower sample rate (try 16000)
    * Import pre-installed libraries:
        * `import board, audiocore, audiopwmio`
    * Load the music file:
        * `music = audiocore.WaveFile("my_wav_file.wav")`
    * Configure audio (on our boards, the piezo buzzer is GP pin 22):
        * `audio = audiopwmio.PWMAudioOut(board.GP22)`
    * Play the music file once:
        * `audio.play(music)`
    * Play the music file on repeat:
        * `audio.play(music, loop=True)`
    * See reference documentation for the [audiocore](https://docs.circuitpython.org/en/latest/shared-bindings/audiocore) and [audiopwmio](https://docs.circuitpython.org/en/latest/shared-bindings/audiopwmio) libraries 

??? note "Play Music from a MP3 audio file"

    * Note: You will probably need to edit/convert your MP3 file before playing it.
    * We recommend using the excellent free program [Audacity](https://www.audacityteam.org) to edit/convert MP3 files
    * Export your MP3 file with these settings:
        * Mono channel (not stereo)
        * Constant Bit Rate Mode (not preset, variable, or average)
        * Lower Sample Rate (try 11025, other values may work too)
        * Lower Quality (try 32 kbps, other values may work too)
    * Import pre-installed libraries:
        * `import board, audiomp3, audiopwmio`
    * Load the music file:
        * `music = audiomp3.MP3Decoder("my_mp3_file.wav")`
    * Configure audio (on our boards, the piezo buzzer is GP pin 22):
        * `audio = audiopwmio.PWMAudioOut(board.GP22)`
    * Play the music file once:
        * `audio.play(music)`
    * Play the music file on repeat:
        * `audio.play(music, loop=True)`
    * See reference documentation for the [audiomp3](https://docs.circuitpython.org/en/latest/shared-bindings/audiomp3) and [audiopwmio](https://docs.circuitpython.org/en/latest/shared-bindings/audiopwmio) libraries

??? note "Using Mixers for music"

    * You can use mixers along with MP3 or WAV files to play mix them or change the volume
    * Initialize music and audio like how you would when playing them normally
    * Initialize the mixer
        * `mixer = audiomixer.Mixer(voice_count, sample_rate, channel_count, bits_per_sample, samples_signed)`
    * Play the mixer using the audio
        * `audio.play(mixer)`
    * Play the music using the mixer
        * `mixer.voice[index].play(music)`
        * index: what voice you want to use for that mixer
    * Change volume of music
        * `mixer.voice[index].level = 0.5`
        * Takes decimal values between 0 and 1, 0 being muted and 1 being full volume.
