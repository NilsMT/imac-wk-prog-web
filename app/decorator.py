from functools import wraps
from flask import abort, session, render_template

#https://stackoverflow.com/questions/26736419/how-to-write-flask-decorator-with-request

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get("user")
        if not user:
            return render_template("pages/no-auth.html")
        return f(*args, **kwargs)
    return decorated_function

def active_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get("user")
        if not user or user["active"] == 0:
            return render_template("pages/no-auth.html")
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get("user")
        if not user or user["admin"] != 1:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function