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

#services
import service.auth
import model.auth
import service.user
import service.event

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

#try to login
#if fail, redirect to inscription thing
@app.route("/user/login", methods=['POST'])
def loginUser():
    email = password = ""

    try:
        email = request.form["email"]
        password = request.form["password"]
    except:
        return jsonify({"message" : "Login failure : request malformed/incomplete"}),400
    
    user, status = service.auth.tryToLogin(email,password)
    
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

#register account
@app.route("/user/register", methods=['POST'])
def registerUser():
    email = password = name = firstname = promo = pseudo = ""

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

    try:
        email = request.form["email"]
    except:
        return jsonify({"message" : "Register failure : request malformed/incomplete"}),400
    
    status = service.user.deleteUser(email)

    match status:
        case 0:
            return jsonify({"message" : "Deletion success"}),200
        case 1:
            return jsonify({"message" : "Deletion failure : user doesn't exist"}),404
        case _:
            return jsonify({"message" : "Deletion failure : unknown returned status"}),500

############################
# event routes
############################
#create event
@app.route("/event", method=['POST'])
def createEvent():
    user = session.get("user")
    data_event = request.form

    messsage, status = service.event.createEvent(data_event, user["id_user"])
    return jsonify({"message" : messsage}), status

#delete event
@app.route("/event/<int:id_event>", method=['DELETE'])
def deleteEvent(id_event):
    user = session.get("user")

    messsage, status = service.event.deleteEvent(id_event, user["id_user"])
    return jsonify({"message" : messsage}), status

#update event
@app.route("/event/<int:id_event>", method=['PUT'])
def updateEvent(id_event):
    user = session.get("user")
    data_event = request.form

    messsage, status = service.event.updateEvent(data_event, id_event, user["id_user"])
    return jsonify({"message" : messsage}), status

# get events
@app.route("/event/all", method=['GET'])
def getAllEvents():
    objects, status = service.event.getAllEvents()
    match status:
        case 200:
            return jsonify(objects), status
        case _:
            return jsonify(objects), 500

@app.route("/event/allNext", method=['GET'])
def getAllNextEvents():
    objects, status = service.event.getAllNextEvents()
    match status:
        case 200:
            return jsonify(objects), status
        case _:
            return jsonify(objects), 500

@app.route("/event/myNext", method=['GET'])
def getNextEvent():
    user = session.get("user")

    objects, status = service.event.getNextEvent(user["id_user"])
    match status:
        case 200:
            return jsonify(objects), status
        case _:
            return jsonify(objects), 500

@app.route("/event/myEvents", method=['GET'])
def getMyEvents():
    user = session.get("user")

    objects, status = service.event.getMyEvents(user["id_user"])
    match status:
        case 200:
            return jsonify(objects), status
        case _:
            return jsonify(objects), 500

#############################
#special behaviors
#############################
@app.teardown_appcontext
def on_close(exception):
    database.disconnect_db()