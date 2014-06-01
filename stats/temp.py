import smbus
from util import Window
import settings
from stats.stat_collector import StatCollector
from time import sleep
import os
import glob
import time



class TempCollector(StatCollector):

    def __init__(self):
        self.window = Window()
        self.name = 'temp'
        self.file = settings.temp_file

        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        self.base_dir = '/sys/bus/w1/devices/'
        self.device_folder = glob.glob(self.base_dir + '28*')[0]
        self.device_file = self.device_folder + '/w1_slave'
        

    def read_temp_raw(self):
        with open(self.device_file, 'r') as f:
            return f.readlines()

    def collect(self, bus):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            self.window.add(temp_f)
