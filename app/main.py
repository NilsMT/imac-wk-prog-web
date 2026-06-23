#############################
#init and imports
#############################

import sys, os
#to be able to do service.XXX
sys.path.insert(0, os.path.dirname(__file__))

#import
from flask import Flask, render_template, jsonify, request
import crypto
import database

#services
import service.example
import service.auth
import service.user

app = Flask(__name__)

#############################
#pages routes
#############################

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/example") # exemple avec utilisation de service
def example():
    return render_template("example.html", author = service.example.getAuthors())

@app.route("/auth_test") # test auth
def auth_test():
    return render_template("auth_test.html")

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
    
    status = service.auth.tryToLogin(email,password)
    
    match status:
        case 0:
            return jsonify({"message" : "Login success"}),200
        case 1:
            return jsonify({"message" : "Login failure : wrong credential"}),401
        case 2:
            return jsonify({"message" : "Login failure : user doesn't exist"}),404
        case _:
            return jsonify({"message" : "Login failure : unknown returned status"}),500

#disconnect
@app.route("/user/logout", methods=['GET'])
def logoutUser():
    pass #TODO: handle logout

#############################
#user routes
#############################

#register account
@app.route("/user/register", methods=['POST'])
def registerUser():
    email = password = name = firstname = promo = pseudo = ""

    try:
        email = request.form["email"]
        password = request.form["password"] #NOTE: should be pre-hashed by the form ?
        name = request.form["name"]
        firstname = request.form["firstname"]
        promo = request.form["promo"]
        pseudo = request.form["pseudo"]
    except:
        return jsonify({"message" : "Register failure : request malformed/incomplete"}),400
    
    status = service.user.registerUser(email,password,name,firstname,promo,pseudo)

    match status:
        case 0:
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

#############################
#special behaviors
#############################
@app.teardown_appcontext
def on_close(exception):
    database.disconnect_db()