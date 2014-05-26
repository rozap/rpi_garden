from time import sleep



import smbus


DEVICE_ADDRESS = 0x4d 
DEVICE_REG_MODE1 = 0x00
DEVICE_REG_LEDOUT0 = 0x1d


def main():
    bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)




    while True:
        print "Reading PH"
        bytes = bus.read_byte_data(DEVICE_ADDRESS, 2)
        print bytes
        sleep(1)


if __name__ == '__main__':
    main()