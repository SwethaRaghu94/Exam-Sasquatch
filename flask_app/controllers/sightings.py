from flask import render_template, redirect, request, session, flash

from flask_app.models.sighting import Sighting

from flask_app import app
from datetime import datetime


from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/dashboard")
def show_all_sightings():
    if "user_id" not in session:
        return redirect("/")
    sightings = Sighting.get_all()
    print("this")
    return render_template("all_sightings.html", sightings=sightings)


@app.route("/create")
def create():
    if "user_id" not in session:
        return redirect("/")
    user_id = session["user_id"]
    return render_template("add_sighting.html")


@app.route("/create", methods=["POST"])
def report_sighting():
    if "user_id" not in session:
        return redirect("/")
    user_id = session["user_id"]

    if not Sighting.validate_sighting(request.form):
        return redirect("/create")

    data = {
        "location": request.form["location"],
        "date_of_sighting": request.form["date_of_sighting"],
        "number_of_sasquatches": request.form["number_of_sasquatches"],
        "what_happened": request.form["what_happened"],
        "user_id": user_id,
    }
    Sighting.save(data)
    print(data)
    return redirect("/dashboard")


@app.route("/sightings/<int:sighting_id>")
def get_one(sighting_id):
    if "user_id" not in session:
        return redirect("/")
    user_id = session["user_id"]

    sighting = Sighting.get_by_id(sighting_id)
    print("inside get one")
    print(sighting)
    return render_template("readone.html", sighting=sighting)


@app.route("/sightings/edit/<int:sighting_id>")
def edit_sighting(sighting_id):
    if "user_id" not in session:
        return redirect("/")
    user_id = session["user_id"]
    sighting = Sighting.get_by_id(sighting_id)
    return render_template("edit_sighting.html", sighting=sighting)


@app.route("/sightings/edit/<int:sighting_id>", methods=["POST"])
def update(sighting_id):
    if "user_id" not in session:
        return redirect("/")
    user_id = session["user_id"]

    if not Sighting.validate_sighting(request.form):
        return redirect(f"/sightings/edit/{sighting_id}")

    sighting_data = {
        "id": sighting_id,
        "location": request.form["location"],
        "date_of_sighting": request.form["date_of_sighting"],
        "number_of_sasquatches": request.form["number_of_sasquatches"],
        "what_happened": request.form["what_happened"],
        "user_id": user_id,
    }

    Sighting.update(sighting_data)
    return redirect(f"/sightings/{sighting_id}")


@app.route("/sighting/<int:sighting_id>/destroy")
def delete_sighting(sighting_id):
    print("inside destroy")
    Sighting.delete(sighting_id)
    return redirect("/dashboard")
