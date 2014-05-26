from time import sleep



import smbus


DEVICE_ADDRESS = 0x4d 
DEVICE_REG_MODE1 = 0x00
DEVICE_REG_LEDOUT0 = 0x1d

v_ref = 3.203
op_amp_gain = 5.25 

ph7_cal = 2951.0
ph4_cal = 1286.0
ph_step = 59.16



def calculate_slope():
    ph_step = ((((v_ref * (ph7_cal - ph4_cal)) / 4096.0) * 1000.0) / op_amp_gain) / 3


def calibrate_ph4(cal_num):
    ph4_cal = cal_num
    calculate_slope()

def calibrate_ph7(cal_num):
    ph7_cal = cal_num
    calculate_slope()

def calculate_ph(res):
    print "res is %s" % res
    millivolts = (res / 4096.0) * v_ref * 1000.0
    temp = ((((v_ref * ph7_cal) / 4096.0) * 1000.0) - millivolts) / op_amp_gain
    ph = 7.0 - (temp / ph_step)
    return ph



def main():
    bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)




    while True:
        print "Reading PH"
        bytes = bus.read_i2c_block_data(DEVICE_ADDRESS, 1)
        hi = bytes[0]
        lo = bytes[1]
        adc_res = (hi * 256.0) + lo
        ph = calculate_ph(adc_res)
        print "Ph is %s" % str(ph)
        sleep(1)


if __name__ == '__main__':
    main()
