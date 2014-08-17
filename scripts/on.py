import RPi.GPIO as GPIO
from time import sleep



PUMP = 26
VALVE = 24
LIGHTS = 22


def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PUMP, GPIO.OUT)
    GPIO.setup(VALVE, GPIO.OUT)
    GPIO.setup(LIGHTS, GPIO.OUT)


def stop(t):
    GPIO.output(PUMP, GPIO.LOW)
    GPIO.output(VALVE, GPIO.LOW)
    GPIO.output(LIGHTS, GPIO.LOW)
    sleep(t)

def drain(duration):
    GPIO.output(PUMP, GPIO.LOW)
    GPIO.output(VALVE, GPIO.HIGH)
    sleep(duration)
    stop(0)



def light(t):
    GPIO.output(LIGHTS, GPIO.HIGH)
    sleep(t)
    stop(0)

def fill(duration):
    GPIO.output(VALVE, GPIO.LOW)
    GPIO.output(PUMP, GPIO.HIGH)
    sleep(duration)
    stop(0)



def main():
    init()
    for i in range(0, 5):
	print "FILLING"
        fill(5)
	print "STOPPING"
        stop(5)
if __name__ == '__main__':
    main()
