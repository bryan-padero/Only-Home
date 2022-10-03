from flask import Blueprint, render_template, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from website.forms import LoginForm, RegisterForm
from website.models.user import User
from website.extensions import db


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST", "GET"])
def login():
    login_form = LoginForm()
    register_form = RegisterForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if not user:
            flash("Email does not exist", "danger")
            return redirect(url_for("auth.login"))
        elif not check_password_hash(user.password, login_form.password.data):
            flash("Password incorrect, please try again", "danger")
            return redirect(url_for("auth.login"))
        else:
            remember_me = True if request.form.get("remember") else False
            login_user(user, remember=remember_me)
            return redirect(url_for("account.update_profile"))
    return render_template("login_page.html", login_form=login_form, register_form=register_form)


@auth.route("/register", methods=["POST", "GET"])
def register():
    register_form = RegisterForm()
    login_form = LoginForm()
    if register_form.validate_on_submit():
        if User.query.filter_by(email=register_form.email.data).first():
            flash("Email address already in use, please try again", "danger")
            return redirect(request.url)
        if register_form.password.data == register_form.confirm_password.data:
            hashed_and_salted_password = generate_password_hash(register_form.password.data,
                                                                method="pbkdf2:sha256",
                                                                salt_length=8)
            new_user = User()
            new_user.email = register_form.email.data
            new_user.password = hashed_and_salted_password
            new_user.first_name = register_form.first_name.data.title()
            new_user.last_name = register_form.last_name.data.title()
            db.session.add(new_user)
            db.session.commit()
            flash("User registered successfully", "success")
            return redirect(request.url)
        else:
            flash("Password does not match, please try again", "danger")
            return redirect(request.url)
    return render_template("login_page.html", login_form=login_form, register_form=register_form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('account.index'))
