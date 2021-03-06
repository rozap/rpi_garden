from flask import Flask, render_template
from api.api import Api
from timelapse import Timelapse
import sys
from time import mktime
from datetime import datetime
import logging
import logging.handlers

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


def now():
    return int(mktime(datetime.now().timetuple()))


def setup_logger():
    my_logger = logging.getLogger('garden_log')
    my_logger.setLevel(logging.DEBUG)
    handler = logging.handlers.SysLogHandler(address = '/dev/log')
    my_logger.addHandler(handler)
    my_logger.info('Logging started')
    return my_logger

class State(object):

    def __init__(self):
        self.state = {
            'action' : 'sitting',
            'duration' : 100,
            'now' : now()
        }

    def set(self, action, duration):
        self.state['action'] = action
        self.state['started'] = now()
        self.state['duration'] = duration

    def get(self):
        self.state['now'] = now() 
        return self.state



if __name__ == "__main__":
    print "STARTING"
    print sys.argv
    logger = setup_logger()
    state = State()
    threads = []
    if not len(sys.argv) == 2 or not sys.argv[1] == 'web':
        from stats.collector import CollectionManager
        from cycle import Cycle
        from light import Lights
        from feeder import Feeder
        threads.append(CollectionManager(logger))
        threads.append(Cycle(state, logger))
        threads.append(Lights(state, logger))
	threads.append(Feeder(state, logger))
    Api(app, state)
    threads.append(Timelapse(logger))
    print "Running web app..."
    app.run(host = '0.0.0.0', debug = False)
    print "Done..."
