from flask import Flask, request
from manage_process import Manage

"""
    Create new instance of Manage for manage process.
"""
manage_procs = Manage()
app = Flask(__name__)


# Welcome page
@app.route("/")
def index():
    return "Welcome the Distributed Project Web Services"


@app.route("/predict", methods=['POST', 'GET'])
def predict():
    return "If you want to predict an image with your web or desktop app, you can make predict under this url."


if __name__ == "__main__":
    if manage_procs.start():
        print("Application is starting...")
        app.run()   # start flask web service
    else:
        print("While occurs error connecting to mongodb or authentication to twitter...")
