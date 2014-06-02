import smbus
import json
DEVICE_ADDRESS = 0x4d 




def main():
    bus = smbus.SMBus(1)

    adc_res = 0.0
    for i in range(0, 20):
        bytes = bus.read_i2c_block_data(DEVICE_ADDRESS, 1)
        hi = bytes[0]
        lo = bytes[1]
        adc_res += (hi * 256.0) + lo

    res = adc_res / 20
    print "Res is %s" % res

    hi_lo, known_ph = raw_input("Enter <hi or lo>, <known>").split(',')


    with open('../data/ph_calibration.json', 'r+') as f:
        existing = json.loads(f.read())
        f.seek(0)
        existing['ph_%s_cal' % hi_lo] = res
        existing['ph_%s_known' % hi_lo] = known_ph
        f.write(json.dumps(existing))
        f.truncate()
        print "New config is..."
        print existing





if __name__ == '__main__':
    main()
