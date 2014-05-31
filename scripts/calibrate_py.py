import ..settings
import smbus
import json
DEVICE_ADDRESS = 0x4d 




def main():

    adc_res = 0.0
    for i in range(0, 20):
        bytes = bus.read_i2c_block_data(DEVICE_ADDRESS, 1)
        hi = bytes[0]
        lo = bytes[1]
        adc_res += (hi * 256.0) + lo

    res = adc_res / 20

    print "Res is %s" % res
    ph_kind = "ph%s_cal" % int(raw_input("Is this ph4 or ph7"))

    with open(settings.ph_calibration, 'r+') as f:
        existing = json.loads(f.read())
        f.seek(0)
        existing[ph_kind] = res
        f.write(json.dumps())
        print "New config is..."
        print existing





if __name__ == '__main__':
    main()