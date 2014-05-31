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
        self.thread = threading.Thread(target = self.collect, args = (self.collectors,))
        self.thread.start()

    def collect(self, *args, **kwargs):
        collectors = args[0]
        bus = smbus.SMBus(1)
        iteration = 0
        while True:
            for collector in collectors:
                run_success = False
                while not run_success:
                    try:
                        collector.collect(bus)
                        run_success = True
                    except IOError:
                        print "%s failed, running again..." % collector.name
                #never stoppin for nobody
            iteration += 1
            sleep(1)

            [print collector for collector in collectors]

            #only write the value sometimes
            if iteration % 120 == 0:
                for collector in collectors:
                    collector.write()



