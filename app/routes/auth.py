from flask import Blueprint, request, session, jsonify
import service.auth

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/api/v1/session", methods=['POST'])
def loginUser():
    email = password = ""

    try:
        email = request.form["email"]
        password = request.form["password"]
    except:
        return jsonify({"message": "Login failure : request malformed/incomplete"}), 400

    user, status = service.auth.tryToLogin(email, password)

    match status:
        case 0:
            user = dict(user)
            user.pop("password", None)
            if user.get("active") == 0:
                return jsonify({"message": "Votre compte n'est pas encore activé."}), 403
            session["user"] = user
            return jsonify({"message": "Login success"}), 200
        case 1:
            return jsonify({"message": "Login failure : wrong credential"}), 401
        case 2:
            return jsonify({"message": "Login failure : user doesn't exist"}), 404
        case _:
            return jsonify({"message": "Login failure : unknown returned status"}), 500

@auth_bp.route("/api/v1/session", methods=['DELETE'])
def logoutUser():
    session.pop("user", None)
    return jsonify({"message": "Logout success"}), 200
