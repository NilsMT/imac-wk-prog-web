from flask import Blueprint, render_template, session, abort
import service.event
import service.admin
from decorator import login_required, active_required, admin_required

page_bp = Blueprint("page", __name__)

@page_bp.route("/")
@active_required
def index():
    user = session.get("user")
    next_event, err1 = service.event.getNextEvent(user["id_user"])
    events, err2 = service.event.getAllNextEvents()
    error = err1 or err2
    return render_template("pages/dashboard.html", current_user=user, next_event=next_event, events=events, error=error)

@page_bp.route("/login")
def login():
    user = session.get("user")
    if user:
        if user["active"] == 0:
            return render_template("pages/no-auth.html")
        return render_template("pages/dashboard.html", current_user=user)
    return render_template("pages/login.html")

@page_bp.route("/register")
def register():
    user = session.get("user")
    if user:
        if user["active"] == 0:
            return render_template("pages/no-auth.html")
        return render_template("pages/dashboard.html", current_user=user)
    return render_template("pages/register.html")

@page_bp.route("/myEvents")
@login_required
@active_required
def my_events():
    user = session.get("user")
    events, error = service.event.getMyEvents(user["id_user"])
    return render_template("pages/myEvents.html", current_user=user, events=events, error=error)

@page_bp.route("/admin")
@login_required
@admin_required
def admin():
    user = session.get("user")
    users = service.admin.getUsers(user["id_user"])
    return render_template("pages/admin.html", current_user=user, users=users)

@page_bp.route("/createEvent")
@login_required
@active_required
def createEvent():
    user = session.get("user")
    if user:
        return render_template("pages/createEvent.html", current_user=user)
    else :
        return render_template("pages/no-auth.html")

@page_bp.route("/profile")
@login_required
@active_required
def profile():
    user = session.get("user")
    if user:
        return render_template("pages/profile.html", current_user=user)
    else :
        return render_template("pages/no-auth.html")
