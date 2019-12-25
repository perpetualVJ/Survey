import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    address = request.form.get('address')
    pincode = request.form.get('pincode')
    state = request.form.get('state')
    position = request.form.get('position')

    if not name or not phone or not email or not address or not pincode or not state or not position:
        return render_template("error.html", message="Oops!Looks like you haven't submitted required fields")
    file = open("survey.csv","a")
    writer = csv.writer(file)
    writer.writerow((name, position, phone, email, address, pincode, state))
    file.close()
    return redirect("/sheet")

@app.route("/sheet", methods=["GET"])
def get_sheet():
    file = open("survey.csv","r")
    reader = csv.reader(file)
    survey = list(reader)
    return render_template("survey.html", survey = survey)
