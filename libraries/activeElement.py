
'''
Pinball libaray for slingshots and popbumpers

usage:

from activeElement import ActiveElement

popbumper1 = ActiveElement(sensor_pin=board.GP27, solenoid_pin=board.GP4)
slingshot1 = ActiveElement(sensor_pin=board.GP16, solenoid_pin=board.GP17)

while True:
    popbumper1.monitor()
    slingshot1.monitor()

'''


import board
import digitalio
import time

class ActiveElement:

    DEFAULT_ON_SECONDS = 0.020
    DEFAULT_OFF_SECONDS = 0.200

    STATE_IDLE = 0
    STATE_FIRING = 1
    STATE_COOLING = 2

    def __init__(self, sensor_pin, solenoid_pin, on_seconds=DEFAULT_ON_SECONDS, off_seconds=DEFAULT_OFF_SECONDS):

        self.sensor = digitalio.DigitalInOut(sensor_pin)
        self.sensor.direction = digitalio.Direction.INPUT
        self.sensor.pull = digitalio.Pull.UP

        self.solenoid = digitalio.DigitalInOut(solenoid_pin)
        self.solenoid.direction = digitalio.Direction.OUTPUT
        self.solenoid.value = True  # True == Off

        self.on_seconds = on_seconds
        self.off_nanoseconds = off_seconds * 1_000_000_000

        self.last_activated_time = time.monotonic_ns()
        self.state = self.STATE_IDLE

    def monitor(self):
        current_time = time.monotonic_ns()

        if self.state == self.STATE_COOLING:
            if current_time >= self.last_activated_time + self.off_nanoseconds:
                self.state = self.STATE_IDLE

        if self.state == self.STATE_IDLE:
            if self.sensor.value == False:  # False == pressed
                self.state = self.STATE_FIRING
                self.solenoid.value = False    # False == On
                time.sleep(self.on_seconds)
                self.solenoid.value = True    # True == Off
                self.state = self.STATE_COOLING
                self.last_activated_time = time.monotonic_ns()
