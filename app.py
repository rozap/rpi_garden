from flask import Flask, render_template
from api.api import 
from stats.collector import CollectionManager
app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html')

if __name__ == "__main__":
    Api(app)
    collection_manager = CollectionManager()
    collection_manager.start()
    app.run(debug = True)