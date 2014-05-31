import smbus
from util import Window
from .. import settings
from collector import Collector

DEVICE_ADDRESS = 0x70


class LevelCollector(Collector):

    def __init__(self):
        self.window = Window()
        self.name = 'level'
        self.file = settings.level_file
        

    def collect(bus):
        bus.write_byte_data(DEVICE_ADDRESS, 0, 81)
        sleep(.02)
        bytes = bus.read_word_data(DEVICE_ADDRESS, 2) / 255
        self.window.add(bytes)
        self.push_datapoint(self.window.moving_average())
