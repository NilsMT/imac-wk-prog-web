from flask import Blueprint, render_template, session
import service.event

page_bp = Blueprint("page", __name__)

@page_bp.route("/")
def index():
    user = session.get("user")
    if user:
        next_event = service.event.getNextEvent(user["id_user"])[0]
        events = service.event.getAllNextEvents()[0]
        return render_template("pages/dashboard.html", current_user=user, next_event=next_event, events=events)
    else :
        return render_template("pages/no-auth.html")

@page_bp.route("/login")
def login():
    user = session.get("user")
    if user:
        return render_template("pages/dashboard.html", current_user=user)
    else :
        return render_template("pages/login.html")

@page_bp.route("/register")
def register():
    user = session.get("user")
    if user:
        return render_template("pages/dashboard.html", current_user=user)
    else :
        return render_template("pages/register.html")