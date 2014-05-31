import smbus
from util import Window
import settings
from stats.stat_collector import StatCollector
from time import sleep

DEVICE_ADDRESS = 0x70


class LevelCollector(StatCollector):

    def __init__(self):
        self.window = Window()
        self.name = 'level'
        self.file = settings.level_file
        

    def collect(self, bus):
        bus.write_byte_data(DEVICE_ADDRESS, 0, 81)
        sleep(.02)
        bytes = bus.read_word_data(DEVICE_ADDRESS, 2) / 255
        self.window.add(bytes)
        self.push_datapoint(self.window.moving_average())
