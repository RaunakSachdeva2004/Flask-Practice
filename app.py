from flask import Flask

'''
it will create the instance of the flask class, 
which will be the WSGI application
'''
## WSGI APPLICATION
app = Flask(__name__)


@app.route("/")
def welcome():
    return "Welcome to this flask course"

if __name__ == "__main__":
    app.run()
 