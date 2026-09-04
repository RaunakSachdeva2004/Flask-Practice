from flask import Flask,render_template,request

'''
it will create the instance of the flask class, 
which will be the WSGI application
'''
## WSGI APPLICATION
app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template("home.html")


@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/form',methods=["GET","POST"])
def form():
    if request.method=="POST":
        name= request.form["name"]
        email=request.form["email"]
        return f"Name: {name} and Email: {email}"
    return render_template('form.html')


if __name__ == "__main__":
    app.run(debug=True)
 