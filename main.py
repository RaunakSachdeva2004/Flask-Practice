from flask import Flask,render_template

'''
it will create the instance of the flask class, 
which will be the WSGI application
'''
## WSGI APPLICATION
app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template("home.html")


@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")




if __name__ == "__main__":
    app.run(debug=True)
 