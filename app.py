from flask import Flask, render_template
from api.api import Api 
import sys
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    print sys.argv
    if not len(sys.argv) == 2 or not sys.argv[1] == 'web':
        from stats.collector import CollectionManager
        collection_manager = CollectionManager()
    Api(app)
    print "Running web app..."
    app.run(host = '0.0.0.0', debug = True)
