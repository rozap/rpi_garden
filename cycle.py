import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)



while True:
    print "Filling!"
    GPIO.output(26, GPIO.LOW)
    GPIO.output(24, GPIO.HIGH)
    sleep(5000)
    print "Draining!"
    GPIO.output(24, GPIO.LOW)
    GPIO.output(26, GPIO.HIGH)
    sleep(200)
