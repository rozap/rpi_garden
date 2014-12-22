import RPi.GPIO as GPIO
from time import sleep
import threading



LIGHT = 22
LIGHT_DURATION = 3600 * 19
DARK_DURATION = 3600 * 5

class Lights(object):

    def __init__(self, state, logger):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(LIGHT, GPIO.OUT)
        self.logger = logger
        self.thread = threading.Thread(target = self.light)
        self.thread.setDaemon(True)
        self.thread.start()



    def off(self, duration):
        self.logger.info("Lights turned OFF")
        GPIO.output(LIGHT, GPIO.HIGH)
        sleep(duration)



    def on(self, duration):
        self.logger.info("Lights turned ON")
        GPIO.output(LIGHT, GPIO.LOW)
        sleep(duration)
        self.stop()



    def light(self):
        while True:
            self.logger.info("Light Cycle...")
            try:
                self.on(LIGHT_DURATION)
                self.off(DARK_DURATION)
            except Exception as e:
                self.logger.critical(str(e))


