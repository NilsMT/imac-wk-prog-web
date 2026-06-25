from flask import Blueprint, request, session, jsonify
import service.user
import model.auth

user_bp = Blueprint("user", __name__)

@user_bp.route("/api/v1/users", methods=['PUT'])
def updateUser():
    user = session.get("user")
    if not user:
        return jsonify({"message": "Échec : non connecté"}), 401

    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        name = data.get("name")
        firstname = data.get("firstname")
        promo = data.get("promo")
        pseudo = data.get("pseudo")
    except:
        return jsonify({"message": "Échec : requête incomplète ou malformée"}), 400

    status = service.user.updateUser(email, password, name, firstname, promo, pseudo, user["user_id"])

    match status:
        case 0:
            return jsonify({"message": "Mise à jour réussie"}), 200
        case 1:
            return jsonify({"message": "Échec : un compte avec cet email existe déjà"}), 409
        case 2:
            return jsonify({"message": "Échec : un compte avec ce pseudo existe déjà"}), 409
        case _:
            return jsonify({"message": "Échec : statut de retour inconnu"}), 500

@user_bp.route("/api/v1/users", methods=['POST'])
def registerUser():
    try:
        email = request.form["email"]
        password = request.form["password"]
        name = request.form["name"]
        firstname = request.form["firstname"]
        promo = request.form["promo"]
        pseudo = request.form["pseudo"]
    except:
        return jsonify({"message": "Échec : requête incomplète ou malformée"}), 400

    status = service.user.registerUser(email, password, name, firstname, promo, pseudo)

    match status:
        case 0:
            user = dict(model.auth.getUserFromEmail(email))
            user.pop("password", None)
            session["user"] = user
            return jsonify({"message": "Inscription réussie"}), 200
        case 1:
            return jsonify({"message": "Échec : un compte avec cet email existe déjà"}), 409
        case 2:
            return jsonify({"message": "Échec : un compte avec ce pseudo existe déjà"}), 409
        case _:
            return jsonify({"message": "Échec : statut de retour inconnu"}), 500
