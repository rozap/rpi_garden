import RPi.GPIO as GPIO
from time import sleep
import threading



PUMP = 24
VALVE = 21
DRAIN_DURATION = 1000
FILL_DURATION = 84
SIT_DURATION = 200
STOP_DURATION = 0

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
        GPIO.output(PUMP, GPIO.HIGH)
        GPIO.output(VALVE, GPIO.HIGH)
        self.state.set('sitting', duration)
        sleep(duration)



    def drain(self, duration):
        self.logger.info("Starting drain")
        self.state.set('draining', duration)
        GPIO.output(PUMP, GPIO.HIGH)
        GPIO.output(VALVE, GPIO.LOW)
        sleep(duration)
        self.stop()



    def fill(self, duration):
        self.logger.info("Starting fill")
        self.state.set('filling', duration)
        GPIO.output(VALVE, GPIO.HIGH)
        GPIO.output(PUMP, GPIO.LOW)
        sleep(duration)
        self.stop()



    def cycle(self):
        while True:
            self.logger.info("Cycle happening...")
            try:
		self.logger.info("cycle: Filling for %s" % FILL_DURATION)
	        self.fill(FILL_DURATION)
		self.logger.info("cycle: Sitting for %s" % SIT_DURATION)
                self.stop(SIT_DURATION)
		self.logger.info("cycle: Draining for %s" % DRAIN_DURATION)
                self.drain(DRAIN_DURATION)
		self.logger.info("cycle: Stopping for %s" % STOP_DURATION)
		self.stop(STOP_DURATION)
            except Exception as e:
                self.logger.critical(str(e))


