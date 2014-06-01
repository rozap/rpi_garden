from flask import Flask, render_template
from api.api import Api 
import sys
from time import mktime
from datetime import datetime
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


def now():
    return int(mktime(datetime.now().timetuple()))

class State(object):

    def __init__(self):
        self.state = {
        'draining' : {
            'is' : True,
            'duration' : 0,
            'started' : now()
            }, 
        'filling' : {
            'is' : False, 
            'duration' : 0, 
            'started' : now()
            }
        }

    def set(self, state):
        self.state = state

    def get(self):
        return self.state

    def set_filling(self, b, duration):
        self.state['draining']['is'] = False
        self.state['filling'] = {
            'is' : b,
            'duration' : duration,
            'started' : now()
        }

    def set_draining(self, b, duration):
        self.state['filling']['is'] = False
        self.state['draining'] = {
            'is' : b,
            'duration' : duration,
            'started' : now()
        }



if __name__ == "__main__":
    print sys.argv
    state = State()
    if not len(sys.argv) == 2 or not sys.argv[1] == 'web':
        from stats.collector import CollectionManager
        from cycle import Cycle
        collection_manager = CollectionManager()
        cycle = Cycle(state)
    Api(app, state)
    print "Running web app..."
    app.run(host = '0.0.0.0', debug = True)
