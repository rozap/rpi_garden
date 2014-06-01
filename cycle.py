import RPi.GPIO as GPIO
from time import sleep
import threading



PUMP = 26
VALVE = 24
DRAIN_DURATION = 2400
FILL_DURATION = 1200

class Cycle(object):

    def __init__(self, state, logger):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PUMP, GPIO.OUT)
        GPIO.setup(VALVE, GPIO.OUT)
        self.logger = logger
        self.state = state
        self.thread = threading.Thread(target = self.cycle)
        self.thread.start()




    def stop(self):
        self.logger.info("Drain and pump off")
        GPIO.output(PUMP, GPIO.LOW)
        GPIO.output(VALVE, GPIO.LOW)
        self.state.set_draining(False)
        self.state.set_filling(False)



    def drain(self, duration):
        self.logger.info("Starting drain")
        self.state.set_draining(True, duration)
        GPIO.output(PUMP, GPIO.LOW)
        GPIO.output(VALVE, GPIO.HIGH)
        sleep(duration)
        self.stop()



    def fill(self, duration):
        self.logger.info("Starting fill")
        self.state.set_filling(True, duration)
        GPIO.output(VALVE, GPIO.LOW)
        GPIO.output(PUMP, GPIO.HIGH)
        sleep(duration)
        self.stop()



    def cycle(self):
        while True:
            self.logger.info("Cycle happening...")
            try:
                self.drain(DRAIN_DURATION)
                self.fill(FILL_DURATION)
            except Exception as e:
                self.logger.critical(str(e))


