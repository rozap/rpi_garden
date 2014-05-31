from datetime import datetime
from time import mktime, sleep
import json

class StatCollector(object):

    def push_datapoint(self, value):
        with open('%s' % self.file, 'r+') as f:
            try:
                existing = json.loads(f.read())
            except ValueError:
                existing = []
            timestamp = int(mktime(datetime.now().timetuple()))
            existing.insert(0, {'time' : timestamp, self.name : value})
            f.seek(0)
            updated = json.dumps(existing)
            f.write(updated)

    def write(self):
        self.push_datapoint(self.window.moving_average())

    def __str__(self):
        return "%s is %s" % (self.name, self.window.moving_average())
