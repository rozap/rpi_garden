import json
from datetime import datetime
from time import mktime
import os

class Logger(object):

    def __init__(self, name):
        self.name = name

    #This is mega inefficient, good thing idgaf
    def write(self, value):

        timestamp = int(mktime(datetime.now().timetuple()))
        sample = {'time' : timestamp, self.name : value}
        filename = 'data/%s.json' % self.name
        if not os.path.isfile(filename):
            open(filename, 'w+').close()

        with open(filename, 'r+') as f:
            try:
                c = f.read()
                series = json.loads(c)
                series.insert(0, sample)
            except ValueError as e:
                series = [sample]
            f.seek(0)
            f.write(json.dumps(series))



