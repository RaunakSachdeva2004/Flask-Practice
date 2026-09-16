import os
from flask import Flask, render_template, request

"""
Handling HTTP Methods (GET & POST) and form submissions in Flask.
"""
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)


@app.route("/")
def welcome():
    return render_template("home.html")


@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        return f"Hello {name}! Received email: {email}"
    return render_template("form.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        return f"Name: {name} and Email: {email}"
    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)
