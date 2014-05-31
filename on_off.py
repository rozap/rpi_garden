import RPi.GPIO as GPIO
from time import sleep



PUMP = 24
VALVE = 26



def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PUMP, GPIO.OUT)
    GPIO.setup(VALVE, GPIO.OUT)



def stop():
    GPIO.output(PUMP, GPIO.LOW)
    GPIO.output(VALVE, GPIO.LOW)


def drain(duration):
    GPIO.output(PUMP, GPIO.LOW)
    GPIO.output(VALVE, GPIO.HIGH)
    sleep(duration)
    stop()



def fill(duration):
    GPIO.output(VALVE, GPIO.LOW)
    GPIO.output(PUMP, GPIO.HIGH)
    sleep(duration)
    stop()



def main():
    init()
    stop()


    while True:
	fill(1000)
	drain(500)

if __name__ == '__main__':
    main()
