from flask import Blueprint, render_template, redirect, url_for, request, flash
from os import path
from uuid import uuid4
from flask_login import login_user, logout_user
from src.models import User
from src.views.auth.forms import RegisterForm, LoginForm
from src.config import Config

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        found_user = User.query.filter(User.username == form.username.data).first()
        if found_user and found_user.check_password(form.password.data):
            login_user(found_user)
            next = request.args.get('next')
            if next:
                return redirect(next)
            return redirect(url_for("main.index"))
        else:
            flash("Credentials wrong")
    return render_template("auth/login.html", form=form)



@auth_blueprint.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        new_user.create()
        return redirect(url_for("main.index"))
    return render_template("auth/register.html", form=form)

@auth_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("main.index"))