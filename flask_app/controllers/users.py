from flask import render_template, redirect, request, session, flash

from flask_app.models.user import User

from flask_app import app

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

from flask_app.models.user import User

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    if not User.validate_user(request.form):
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    print(pw_hash)

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash,
    }

    user_id = User.save(data)

    session["user_id"] = user_id

    # User.save(request.form)
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    # if not User.validate_user(request.form):
    #     return redirect("/")
    login_data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(login_data)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Email/Password")
        return redirect("/")

    session["user_id"] = user_in_db.id
    session["first_name"] = user_in_db.first_name
    session["last_name"] = user_in_db.last_name

    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")