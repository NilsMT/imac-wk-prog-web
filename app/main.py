#############################
#init and imports
#############################

import sys, os
#to be able to do service.XXX
sys.path.insert(0, os.path.dirname(__file__))

#import
from flask import Flask, render_template, jsonify, request, session
import crypto
import database
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

#############################
#pages routes
#############################

#routes
@app.route("/")
def index():
    user = session.get("user")
    if user:
        return render_template("pages/dashboard.html", current_user=user)
    else :
        return render_template("pages/no-auth.html")

@app.route("/login")
def login():
    user = session.get("user")
    if user:
        return render_template("pages/dashboard.html", current_user=user)
    else :
        return render_template("pages/login.html")

@app.route("/register")
def register():
    user = session.get("user")
    if user:
        return render_template("pages/dashboard.html", current_user=user)
    else :
        return render_template("pages/register.html")

#############################
#auth routes
#############################
import service.auth
import model.auth

@app.route("/user/login", methods=['POST'])
def loginUser():
    email = password = ""

    #form data retrieval
    try:
        email = request.form["email"]
        password = request.form["password"]
    except:
        return jsonify({"message" : "Login failure : request malformed/incomplete"}),400
    
    user, status = service.auth.tryToLogin(email,password)
    
    #status handling
    match status:
        case 0:
            user = dict(user)
            user.pop("password", None)
            session["user"] = user
            return jsonify({"message" : "Login success"}),200
        case 1:
            return jsonify({"message" : "Login failure : wrong credential"}),401
        case 2:
            return jsonify({"message" : "Login failure : user doesn't exist"}),404
        case _:
            return jsonify({"message" : "Login failure : unknown returned status"}),500

#disconnect
@app.route("/user/logout", methods=['DELETE'])
def logoutUser():
    session.pop("user", None)
    return jsonify({"message" : "Logout success"}),200

#############################
#user routes
#############################
import service.user

#register account
@app.route("/user/register", methods=['POST'])
def registerUser():
    email = password = name = firstname = promo = pseudo = ""

    #form data retrieval
    try:
        email = request.form["email"]
        password = request.form["password"]
        name = request.form["name"]
        firstname = request.form["firstname"]
        promo = request.form["promo"]
        pseudo = request.form["pseudo"]
    except:
        return jsonify({"message" : "Register failure : request malformed/incomplete"}),400
    
    status = service.user.registerUser(email,password,name,firstname,promo,pseudo)

    #status handling
    match status:
        case 0:
            user = dict(model.auth.getUserFromEmail(email))
            user.pop("password", None)
            session["user"] = user
            return jsonify({"message" : "Register success"}),200
        case 1:
            return jsonify({"message" : "Register failure : user with that email already exist"}),409
        case 2:
            return jsonify({"message" : "Register failure : user with that pseudo already exist"}),409
        case _:
            return jsonify({"message" : "Register failure : unknown returned status"}),500
        
#delete account
@app.route("/user/delete", methods=['DELETE'])
def deleteUser():
    email = ""

    #form data retrieval
    try:
        email = request.form["email"]
    except:
        return jsonify({"message" : "Register failure : request malformed/incomplete"}),400
    
    status = service.user.deleteUser(email)

    #status handling
    match status:
        case 0:
            return jsonify({"message" : "Deletion success"}),200
        case 1:
            return jsonify({"message" : "Deletion failure : user doesn't exist"}),404
        case _:
            return jsonify({"message" : "Deletion failure : unknown returned status"}),500

#############################
#participate routes
#############################
import service.participation

@app.route("/participation/add", methods=['POST'])
def addParticipation():
    id_event = ""

    #session retrieval
    user = session.get("user")
    if not user:
        return jsonify({"message": "Participation failure : not logged in"}), 401
    
    #form data retrieval
    try:
        id_event = request.form["id_event"]
    except:
        return jsonify({"message": "Participation failure : request malformed/incomplete"}), 400

    status = service.participation.addParticipation(user["id_user"], id_event)

    #status handling
    match status:
        case 0:
            return jsonify({"message": "Participation added successfully"}), 200
        case 1:
            return jsonify({"message": "Participation failure : already registered"}), 409
        case _:
            return jsonify({"message": "Participation failure : unknown returned status"}), 500


@app.route("/participation/remove", methods=['DELETE'])
def removeParticipation():
    id_event = ""

    #session retrieval
    user = session.get("user")
    if not user:
        return jsonify({"message": "Removal failure : not logged in"}), 401

    #form data retrieval
    try:
        id_event = request.form["id_event"]
    except:
        return jsonify({"message": "Removal failure : request malformed/incomplete"}), 400

    status = service.participation.removeParticipation(user["id_user"], id_event)

    #status handling
    match status:
        case 0:
            return jsonify({"message": "Participation removed successfully"}), 200
        case 1:
            return jsonify({"message": "Removal failure : participation doesn't exist"}), 404
        case _:
            return jsonify({"message": "Removal failure : unknown returned status"}), 500

#############################
#special behaviors
#############################
@app.teardown_appcontext
def on_close(exception):
    database.disconnect_db()