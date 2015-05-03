import RPi.GPIO as GPIO
from time import sleep
import threading



FEEDER = 23
FEED_DURATION = 4
WAIT_DURATION = 3600 * 12

class Feeder(object):

    def __init__(self, state, logger):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(FEEDER, GPIO.OUT)
        self.logger = logger
        self.thread = threading.Thread(target = self.feed)
        self.thread.setDaemon(True)
        self.thread.start()



    def off(self, duration):
        self.logger.info("Feeder turned off")
        GPIO.output(FEEDER, GPIO.HIGH)
        sleep(duration)



    def on(self, duration):
        self.logger.info("Feeder turned on")
        GPIO.output(FEEDER, GPIO.LOW)
        sleep(duration)



    def feed(self):
        while True:
            self.logger.info("Feeder Cycle...")
            try:
                self.on(FEED_DURATION)
                self.off(WAIT_DURATION)
            except Exception as e:
                self.logger.critical(str(e))


