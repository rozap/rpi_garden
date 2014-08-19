import RPi.GPIO as GPIO
from time import sleep



PUMP = 26
VALVE = 24
LIGHTS = 22


def init():
    GPIO.setmode(GPIO.BOARD)



def thing(pin, mode, duration):
    print "Setting %s to %s for %s" % (pin, mode, duration)
    val = GPIO.HIGH if mode == 'hi' else GPIO.LOW
    if not setup.get(pin, False):
        GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, val)
    sleep(duration)


def main():
    init()
    setup = {}
    global setup
    while True:
        [pin, mode, duration] = raw_input("pin mode (lo/hi) duration:\n").split(' ')
        thing(int(pin), mode, int(duration))


if __name__ == '__main__':
    main()
