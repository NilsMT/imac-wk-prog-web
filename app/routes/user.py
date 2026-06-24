from flask import Blueprint, request, session, jsonify
import service.user
import model.auth

user_bp = Blueprint("user", __name__)

@user_bp.route("/user/register", methods=['POST'])
def registerUser():
    try:
        email = request.form["email"]
        password = request.form["password"]
        name = request.form["name"]
        firstname = request.form["firstname"]
        promo = request.form["promo"]
        pseudo = request.form["pseudo"]
    except:
        return jsonify({"message": "Register failure : request malformed/incomplete"}), 400

    status = service.user.registerUser(email, password, name, firstname, promo, pseudo)

    match status:
        case 0:
            user = dict(model.auth.getUserFromEmail(email))
            user.pop("password", None)
            session["user"] = user
            return jsonify({"message": "Register success"}), 200
        case 1:
            return jsonify({"message": "Register failure : user with that email already exist"}), 409
        case 2:
            return jsonify({"message": "Register failure : user with that pseudo already exist"}), 409
        case _:
            return jsonify({"message": "Register failure : unknown returned status"}), 500

@user_bp.route("/user/delete", methods=['DELETE'])
def deleteUser():
    try:
        email = request.form["email"]
    except:
        return jsonify({"message": "Deletion failure : request malformed/incomplete"}), 400

    status = service.user.deleteUser(email)

    match status:
        case 0:
            return jsonify({"message": "Deletion success"}), 200
        case 1:
            return jsonify({"message": "Deletion failure : user doesn't exist"}), 404
        case _:
            return jsonify({"message": "Deletion failure : unknown returned status"}), 500