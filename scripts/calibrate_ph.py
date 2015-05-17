import smbus
import json
from time import sleep
DEVICE_ADDRESS = 0x4d 
NUM_SAMPLES = 40



def main():
    bus = smbus.SMBus(1)

    adc_res = 0.0
    for i in range(0, NUM_SAMPLES):
        bytes = bus.read_i2c_block_data(DEVICE_ADDRESS, 1)
        hi = bytes[0]
        lo = bytes[1]
        adc_res += (hi * 256.0) + lo
        sleep(.5)

    res = adc_res / NUM_SAMPLES
    print "Res is from %s samples is %s" % (NUM_SAMPLES, res)

    known_ph = raw_input("Enter <7 or 4>").strip()
    if known_ph != "7" and known_ph != "4":
        raise "Only use 7 or 4..."


    with open('../data/ph_calibration.json', 'r+') as f:
        existing = json.loads(f.read())
        f.seek(0)
        existing['ph%s_cal' % known_ph] = res
        f.write(json.dumps(existing))
        f.truncate()
        print "New config is..."
        print existing





if __name__ == '__main__':
    main()
