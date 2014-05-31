from flask import Flask, render_template
from api.api import Api 
from stats.collector import CollectionManager
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    Api(app)
    collection_manager = CollectionManager()
    print "Running web app..."
    app.run(host = '0.0.0.0', debug = True)
