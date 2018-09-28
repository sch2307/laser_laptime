#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

class Laser_Module(object):
    def __init__(self, channel):
        self._channel = channel

        # Setup GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._channel, GPIO.OUT)
        GPIO.output(self._channel, GPIO.HIGH)

    def laser_on(self):
        GPIO.output(self._channel, GPIO.LOW)

    def laser_off(self):
        GPIO.output(self._channel, GPIO.HIGH)

    def destroy(self):
        self.laser_off()
        GPIO.cleanup()

if __name__ == '__main__':
    lm = Laser_Module(22)
    try:
        while True:
            lm.laser_on()
    except KeyboardInterrupt:
        lm.destroy()
