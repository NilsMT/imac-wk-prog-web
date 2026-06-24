from flask import Blueprint, render_template, session, abort
import service.event
import service.admin

page_bp = Blueprint("page", __name__)

@page_bp.route("/")
def index():
    user = session.get("user")
    if user:
        if user["active"] == 0:
            return render_template("pages/no-auth.html")
        next_event = service.event.getNextEvent(user["id_user"])[0]
        events = service.event.getAllNextEvents()[0]
        return render_template("pages/dashboard.html", current_user=user, next_event=next_event, events=events)
    else:
        return render_template("pages/no-auth.html")

@page_bp.route("/login")
def login():
    user = session.get("user")
    if user:
        if user["active"] == 0:
            return render_template("pages/no-auth.html")
        else:
            return render_template("pages/dashboard.html", current_user=user)
    else:
        return render_template("pages/login.html")

@page_bp.route("/register")
def register():
    user = session.get("user")
    if user:
        if user["active"] == 0:
            return render_template("pages/no-auth.html")
        else:
            return render_template("pages/dashboard.html", current_user=user)
    else :
        return render_template("pages/register.html")

@page_bp.route("/myEvents")
def my_events():
    user = session.get("user")
    events = service.event.getMyEvents(user["id_user"])[0]
    if user:
        return render_template("pages/myEvents.html", current_user=user, events=events)
    else :
        return render_template("pages/no-auth.html")
    
@page_bp.route("/admin")
def admin():
    user = session.get("user")
    if not user or user["admin"] != 1:
        return abort(403)
    users = service.admin.getUsers(user["id_user"])
    return render_template("pages/admin.html", current_user=user, users=users)

@page_bp.route("/createEvent")
def createEvent():
    user = session.get("user")
    if user:
        return render_template("pages/createEvent.html", current_user=user)
    else :
        return render_template("pages/no-auth.html")
