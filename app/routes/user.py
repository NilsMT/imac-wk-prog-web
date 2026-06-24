from flask import Blueprint, request, session, jsonify
import service.user
import model.auth

user_bp = Blueprint("user", __name__)

#update account
@user_bp.route("/api/v1/users", methods=['PUT'])
def updateUser():
    email = password = name = firstname = promo = pseudo = ""

    #session retrieval
    user = session.get("user")
    if not user:
        return jsonify({"message": "Removal failure : not logged in"}), 401
    
    #form data retrieval
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        name = data.get("name")
        firstname = data.get("firstname")
        promo = data.get("promo")
        pseudo = data.get("pseudo")
    except:
        return jsonify({"message" : "Update failure : request malformed/incomplete"}),400
    
    status = service.user.updateUser(email, password, name, firstname, promo, pseudo, user["user_id"])

    #status handling
    match status:
        case 0:
            return jsonify({"message" : "Update success"}),200
        case 1:
            return jsonify({"message" : "Update failure : user with that email already exist"}),409
        case 2:
            return jsonify({"message" : "Update failure : user with that pseudo already exist"}),409
        case _:
            return jsonify({"message" : "Update failure : unknown returned status"}),500

#register account
@user_bp.route("/api/v1/users", methods=['POST'])
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