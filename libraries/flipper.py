
'''
Flipper library for pinball

usage:

from flipper import Flipper
flipper1 = Flipper(start_pin=board.GP20, stop_pin=board.GP7, solenoid_pin=board.GP28)
while True:
    flipper1.monitor()


notes:
    start_pin is the user-pressed button to fire the flipper
    stop_pin is the sensor on the flipper
    solenoid_pin is the pin that fires the flipper

'''


import board
import digitalio
import pwmio
import time


class Flipper:

    MAX_ON_SECONDS = 0.10

    PWM_FREQUENCY = 50 # in Hertz
    PWM_WEAK_DUTY_CYCLE = int(2**16 * 0.85)  # means 15% power

    STATE_IDLE = 0
    STATE_FIRING_STRONG = 1
    STATE_FIRING_WEAK = 2

    def __init__(self, start_pin, stop_pin, solenoid_pin):

        self.start_button = digitalio.DigitalInOut(start_pin)
        self.start_button.direction = digitalio.Direction.INPUT
        self.start_button.pull = digitalio.Pull.UP

        self.stop_sensor = digitalio.DigitalInOut(stop_pin)
        self.stop_sensor.direction = digitalio.Direction.INPUT
        self.stop_sensor.pull = digitalio.Pull.UP

        self.solenoid_pin = solenoid_pin
        self.solenoid = digitalio.DigitalInOut(solenoid_pin)
        self.solenoid.direction = digitalio.Direction.OUTPUT
        self.solenoid.value = True  # True == Off

        self.max_on_nanoseconds = self.MAX_ON_SECONDS * 1_000_000_000

        self.last_activated_time = time.monotonic_ns()
        self.state = self.STATE_IDLE

    def monitor(self):

        if self.start_button.value == True:  # True == button not pressed

            if self.state == self.STATE_FIRING_STRONG:
                self.solenoid.value = True  # True = Off
                self.state = self.STATE_IDLE
                print("idle")

            if self.state == self.STATE_FIRING_WEAK:
                self.solenoid_pwm.deinit()
                self.solenoid = digitalio.DigitalInOut(self.solenoid_pin)
                self.solenoid.direction = digitalio.Direction.OUTPUT
                self.solenoid.value = True  # True = Off
                self.state = self.STATE_IDLE
                print("idle")


        else: # button is pressed

            if self.state == self.STATE_IDLE:
                print("fire")
                self.solenoid.value = False  # False = On
                self.state = self.STATE_FIRING_STRONG
                self.last_activated_time = time.monotonic_ns()

            elif self.state == self.STATE_FIRING_STRONG:

                if self.stop_sensor.value == True or time.monotonic_ns() > self.last_activated_time + self.off_nanoseconds:  # True = On
                    print("pwm weak mode")
                    self.solenoid.deinit()
                    self.solenoid_pwm = pwmio.PWMOut(self.solenoid_pin, duty_cycle=self.PWM_WEAK_DUTY_CYCLE, frequency=self.PWM_FREQUENCY)
                    self.state = self.STATE_FIRING_WEAK
