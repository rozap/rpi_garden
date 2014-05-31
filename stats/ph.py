import smbus
from util import Window
import settings
from stats.stat_collector import StatCollector
import json
DEVICE_ADDRESS = 0x4d 
DEVICE_REG_MODE1 = 0x00
DEVICE_REG_LEDOUT0 = 0x1d










class PHCollector(StatCollector):

    def __init__(self):
        self.window = Window()
        self.name = 'ph'
        self.file = settings.ph_file
        

    def collect(self, bus):
        #reload config...slower, but allows changes on teh fly
        self.load()


        bytes = bus.read_i2c_block_data(DEVICE_ADDRESS, 1)
        hi = bytes[0]
        lo = bytes[1]
        adc_res = (hi * 256.0) + lo
        ph = self.calculate_ph(adc_res)
        self.window.add(ph)

    def load(self):
        with open(settings.ph_calibration, 'r') as f:
            calibration = json.loads(f.read())
            for key, value in calibration.iteritems():
                setattr(self, key, value)
        self.calculate_slope()

    def calculate_slope(self):
        self.ph_step = ((((self.v_ref * (self.ph7_cal - self.ph4_cal)) / 4096.0) * 1000.0) / self.op_amp_gain) / 3


    def calibrate_ph4(self, cal_num):
        self.ph4_cal = cal_num
        self.calculate_slope()

    def calibrate_ph7(self, cal_num):
        self.ph7_cal = cal_num
        self.calculate_slope()

    def calculate_ph(self, res):
        millivolts = (res / 4096.0) * self.v_ref * 1000.0
        temp = ((((self.v_ref * self.ph7_cal) / 4096.0) * 1000.0) - millivolts) / self.op_amp_gain
        ph = 7.0 - (temp / self.ph_step)
        return ph