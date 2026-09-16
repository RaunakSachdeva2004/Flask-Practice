import os
from flask import Flask, render_template, request, redirect, url_for

"""
Jinja2 Template Engine & Dynamic URL Building in Flask
------------------------------------------------------
Key Jinja2 constructs demonstrated:
1. {{ expression }} : Expression evaluation and output
2. {% condition / loop %} : Control structures (if/else, for loops)
3. {# comment #} : Template comments
4. url_for() : Dynamic URL resolution
5. Variable rules in route decorators (<int:score>)
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


@app.route("/index", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


# 1. Variable Rule with Conditional Template Rendering
@app.route("/success/<int:score>")
def success(score):
    status = "pass" if score >= 50 else "fail"
    return render_template("result.html", results=status)


# 2. Variable Rule with Dictionary Iteration in Template (result1.html)
@app.route("/successres/<int:score>")
def successres(score):
    status = "PASSED" if score >= 50 else "FAILED"
    result_data = {
        "score": score,
        "status": status,
        "passing_threshold": 50
    }
    return render_template("result1.html", results=result_data)


# 3. Form input & grade calculator with dynamic redirect
@app.route("/calculate", methods=["GET", "POST"])
def calculate():
    if request.method == "POST":
        try:
            science = float(request.form.get("science", 0))
            maths = float(request.form.get("maths", 0))
            c_lang = float(request.form.get("c", 0))
            data_science = float(request.form.get("datascience", 0))
            avg_score = int(round((science + maths + c_lang + data_science) / 4))
            return redirect(url_for("successres", score=avg_score))
        except (ValueError, TypeError):
            return render_template("getresult.html", error="Please enter valid numbers.")
    return render_template("getresult.html")


# 4. Standard Form Submission Route
@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        # Supports both simple name/email form and calculate form
        if "science" in request.form:
            return calculate()
        name = request.form.get("name", "Anonymous")
        email = request.form.get("email", "Not provided")
        return f"Form submitted successfully! Name: {name}, Email: {email}"
    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)
