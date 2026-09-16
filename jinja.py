# Building url dynamically
from flask import Flask,render_template,request


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



@app.route('/submit', methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        return f"Name: {name} and Email: {email}"
    return render_template('form.html')

## variable rule
@app.route('/success/<int:score>')
def success(score):
    res=""
    if score>=50:
        res = "pass"
    else:
        res = "fail"
    return render_template('result.html', results = res)


if __name__ == "__main__":
    app.run(debug=True)