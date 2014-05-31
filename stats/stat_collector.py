from datetime import datetime
from time import mktime, sleep
import json

class StatCollector(object):

    def push_datapoint(self, value):
        with open('../data/%s' % self.file, 'r+') as f:
            try:
                existing = json.loads(f.read())
            except ValueError:
                existing = []
            timestamp = int(mktime(datetime.now().timetuple()))
            existing.insert(0, {'time' : timestamp, self.name : value})
            f.seek(0)
            updated = json.dumps(existing)
            f.write(updated)

