"""Musical note library written by Andrew Merrill

Version: 1.0, April 2026

a note is a tuple (letter, octave, duration)
for example, ('A',4,0.1) would be an A note from the 4th octave for a tenth of a second

volume is a number in the range of 0 to 100, inclusive (where 100 is loudest)

usage:
import board, music
music.playNotes(board.GP22, [('C',3,0.1), ('C',4,0.1), ('C',5,0.1)])
"""

import pwmio, microcontroller, time

noteLetters = {'C':-9, 'C#':-8, 'Db':-8, 'D':-7, 'D#':-6, 'Eb':-6, 'E':-5, 'F':-4, 'F#':-3, 'Gb':-3, 'G':-2, 'G#':-1, 'Ab':-1, 'A':0, 'A#':1, 'Bb':1, 'B':2}

def playTone(
    buzzerPin: microcontroller.Pin,
    frequency: int,
    duration: int | float = 0.25,
    volume: int | float = 100,
):
    """
    plays the tone with the given frequency (in hertz), duration (in seconds), and volume (between 0..100)
    uses the buzzer attached to the given GPIO pin
    """
    pwm = pwmio.PWMOut(buzzerPin, duty_cycle=int(327.67 * volume), frequency=frequency)
    time.sleep(duration)
    pwm.deinit()


def playTones(
    buzzerPin: microcontroller.Pin,
    frequencies: list[int],
    duration: int | float = 0.25,
    volume: int | float = 100,
):
    """
    plays the sequence of tones from the given list of frequencies (in hertz)
      using the given duration (in seconds), and volume (between 0..100)
    uses the buzzer attached to the given GPIO pin
    """
    pwm = pwmio.PWMOut(buzzerPin, duty_cycle=int(327.67 * volume), variable_frequency=True)
    for frequency in frequencies:
        pwm.frequency = frequency
        time.sleep(duration)
    pwm.deinit()


def playNote(
    buzzerPin: microcontroller.Pin,
    letter: str,
    octave: int = 4,
    duration: int | float = 0.25,
    volume: int | float = 100,
):
    """
    plays the note with the given letter (like 'A' or 'A#' or 'Ab')
      using the given octave (usually in the range 1..9), duration (in seconds), and volume (between 0..100)
    uses the buzzer attached to the given GPIO pin
    """
    pwm = pwmio.PWMOut(buzzerPin, duty_cycle=int(327.67 * volume), variable_frequency=True)
    pwm.frequency = computeFrequency(letter, octave)
    time.sleep(duration)
    pwm.deinit()


def playNotes(
    buzzerPin: microcontroller.Pin,
    notes: list[tuple[str, int, int | float]],
    volume: int = 100,
):
    """
    plays the notes from the given notes list
       each note is a tuple wigh (letter, octave, duration)
       for example, ('A',4,0.1) would be an A note from the 4th octave for a tenth of a second
    volume is between 0..100
    uses the buzzer attached to the given GPIO pin
    """
    pwm = pwmio.PWMOut(buzzerPin, duty_cycle=int(327.67 * volume), variable_frequency=True)
    for note in notes:
        (letter, octave, duration) = note
        pwm.frequency = computeFrequency(letter, octave)
        time.sleep(duration)
    pwm.deinit()


def computeFrequency(letter: str, octave: int) -> int:
    """
    given a note letter (like 'A' or 'A#' or 'Ab') and an octave number (usually in the range 1..9)
    returns the frequency (in hertz) of that note
    """
    return int(440 * (2 ** (octave-4)) * ((2 ** (1/12)) ** noteLetters[letter]))
