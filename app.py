from flask import Flask, render_template
from api.api import Api 
import sys
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


class State(object):

    def __init__(self):
        self.state = {'draining' : False, 'filling' : False}

    def set(self, state):
        self.state = state

    def get(self):
        return self.state

    def set_filling(self, b):
        self.state['filling'] = b

    def set_draining(self, b):
        self.state['draining'] = b



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
