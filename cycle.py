import RPi.GPIO as GPIO
from time import sleep
import threading



PUMP = 24
VALVE = 26
DRAIN_DURATION = 400
FILL_DURATION = 1200

class Cycle(object):

    def __init__(self, state):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PUMP, GPIO.OUT)
        GPIO.setup(VALVE, GPIO.OUT)
        self.state = state
        self.thread = threading.Thread(target = self.cycle)
        self.thread.start()


    def stop(self):
        GPIO.output(PUMP, GPIO.LOW)
        GPIO.output(VALVE, GPIO.LOW)
        self.state.set_draining(False)
        self.state.set_filling(False)



    def drain(self, duration):
        GPIO.output(PUMP, GPIO.LOW)
        GPIO.output(VALVE, GPIO.HIGH)
        sleep(duration)
        self.stop()



    def fill(self, duration):
        GPIO.output(VALVE, GPIO.LOW)
        GPIO.output(PUMP, GPIO.HIGH)
        sleep(duration)
        self.stop()



    def cycle(self):
        while True:
            self.state.set_draining(True)
            self.drain(DRAIN_DURATION)
            self.state.set_filling(True)
            self.fill(FILL_DURATION)



