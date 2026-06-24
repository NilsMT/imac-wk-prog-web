from flask import Blueprint, render_template, session

page_bp = Blueprint("page", __name__)

@page_bp.route("/")
def index():
    user = session.get("user")
    if user:
        return render_template("pages/dashboard.html", current_user=user)
    else:
        return render_template("pages/no-auth.html")

@page_bp.route("/login")
def login():
    user = session.get("user")
    if user:
        return render_template("pages/dashboard.html", current_user=user)
    else:
        return render_template("pages/login.html")

@page_bp.route("/register")
def register():
    user = session.get("user")
    if user:
        return render_template("pages/dashboard.html", current_user=user)
    else:
        return render_template("pages/register.html")