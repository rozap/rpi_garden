import threading
from datetime import datetime, timedelta
from time import mktime, sleep
import json
from ph import PHCollector
from level import LevelCollector
import smbus

class CollectionManager(object):

    def __init__(self):
            self.collectors = [PHCollector(), LevelCollector()]
            self.thread = threading.Thread(target = self.collect, args = (self.collectors))
            self.thread.start()

    def collect(self, collectors):
        bus = smbus.SMBus(1)
        while True:
            try:
                for collector in collectors:
                    collector.collect(bus)
                sleep(1)
            except Exception as e:
                print e
                #never stoppin for nobody



