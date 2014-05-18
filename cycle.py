import RPi.GPIO as GPIO
from time import sleep



PUMP = 24
VALVE = 26



def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PUMP, GPIO.OUT)
    GPIO.setup(VALVE, GPIO.OUT)


def drain(duration):
    GPIO.output(PUMP, GPIO.LOW)
    GPIO.output(VALVE, GPIO.HIGH)
    sleep(duration)



def fill(duration):
    GPIO.output(VALVE, GPIO.LOW)
    GPIO.output(PUMP, GPIO.HIGH)
    sleep(duration)



def main():
    # init()


    while True:
        try:
            thing, duration = raw_input('Do a thing for <thing, time> :').split(',')
            print "Doing %s for %s seconds" % (thing, duration)
            globals()[thing](duration)
        except (KeyError, ValueError) as e:
            print "Invalid command"
            print e


if __name__ == '__main__':
    main()