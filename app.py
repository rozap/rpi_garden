from flask import Flask
from api.api import Api
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    Api(app)
    app.run(debug = True)