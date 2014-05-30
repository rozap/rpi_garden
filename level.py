from time import sleep
import smbus
from util import Window

DEVICE_ADDRESS = 0x70

def main():
    bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)


    window = Window()


    while True:
        print "Reading Level"
        try:
            bus.write_byte_data(DEVICE_ADDRESS, 0, 81)
            sleep(.02)
            bytes = bus.read_word_data(DEVICE_ADDRESS, 2) / 255
            window.add(bytes)
            sleep(.2)

            print "moving %s avg: %s median %s" % (window.moving_average(), window.average(), window.median())
        except IOError:
            pass


if __name__ == '__main__':
    main()
