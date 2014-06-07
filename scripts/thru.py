import RPi.GPIO as GPIO
from time import sleep



PUMP = 26
VALVE = 24



def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PUMP, GPIO.OUT)
    GPIO.setup(VALVE, GPIO.OUT)



def stop():
    GPIO.output(PUMP, GPIO.LOW)
    GPIO.output(VALVE, GPIO.LOW)


def drain(duration):
    GPIO.output(PUMP, GPIO.HIGH)
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
	stop()
        sleep(5)
	fill(180)
	drain(120)

if __name__ == '__main__':
    main()
