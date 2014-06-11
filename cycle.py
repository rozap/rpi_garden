import RPi.GPIO as GPIO
from time import sleep
import threading



PUMP = 26
VALVE = 24
DRAIN_DURATION = 580
FILL_DURATION = 105
SIT_DURATION = 1000
STOP_DURATION = 120

class Cycle(object):

    def __init__(self, state, logger):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PUMP, GPIO.OUT)
        GPIO.setup(VALVE, GPIO.OUT)
        self.logger = logger
        self.state = state
        self.thread = threading.Thread(target = self.cycle)
        self.thread.setDaemon(True)
        self.thread.start()




    def stop(self, duration = 0):
        self.logger.info("Drain and pump off")
        GPIO.output(PUMP, GPIO.LOW)
        GPIO.output(VALVE, GPIO.LOW)
        self.state.set('sitting', duration)
        sleep(duration)


    def sit(self, duration = 100):
        self.logger.info("Drain and pump off")

        i = 0
        top_duration = 8
        wait_duration = 92
        while i < duration:
            self.fill(top_duration)
            self.stop(wait_duration)
            i += (top_duration + wait_duration)



    def drain(self, duration):
        self.logger.info("Starting drain")
        self.state.set('draining', duration)
        GPIO.output(PUMP, GPIO.LOW)
        GPIO.output(VALVE, GPIO.HIGH)
        sleep(duration)
        self.stop()



    def fill(self, duration):
        self.logger.info("Starting fill")
        self.state.set('filling', duration)
        GPIO.output(VALVE, GPIO.LOW)
        GPIO.output(PUMP, GPIO.HIGH)
        sleep(duration)
        self.stop()



    def cycle(self):
        while True:
            self.logger.info("Cycle happening...")
            try:
            #    self.drain(DRAIN_DURATION)
                self.fill(FILL_DURATION)
                self.sit(SIT_DURATION)
                self.drain(DRAIN_DURATION)
                self.stop(STOP_DURATION)
            except Exception as e:
                self.logger.critical(str(e))


