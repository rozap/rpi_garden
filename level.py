from time import sleep
import smbus


DEVICE_ADDRESS = 0x70

def main():
    bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)




    while True:
        print "Reading PH"
        try:
            bus.write_byte_data(0x70, 0, 81)
            sleep(.02)
            bytes = bus.read_i2c_block_data(DEVICE_ADDRESS, 1)
            print bytes
            sleep(1)
        except IOError:
            print ";_;"


if __name__ == '__main__':
    main()
