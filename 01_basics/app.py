import os
from flask import Flask

"""
Creates an instance of the Flask class, 
which serves as the WSGI application.
"""
app = Flask(__name__)


@app.route("/")
def welcome():
    return "Welcome to this Flask course!"


@app.route("/index")
def index():
    return "Welcome to the index page!"


if __name__ == "__main__":
    app.run(debug=True)
