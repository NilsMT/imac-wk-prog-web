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

    status = service.user.updateUser(email, password, name, firstname, promo, pseudo, user["id_user"])

    match status:
        case 0:
            return jsonify({"message": "Mise à jour réussie"}), 200
        case 1:
            return jsonify({"message": "Échec : un compte avec cet email existe déjà"}), 409
        case 2:
            return jsonify({"message": "Échec : un compte avec ce pseudo existe déjà"}), 409
        case _:
            return jsonify({"message": "Échec : statut de retour inconnu"}), 500

from flask import Blueprint, request, session, jsonify
import service.user
import model.auth
import crypto

user_bp = Blueprint("user", __name__)

@user_bp.route("/api/v1/users", methods=['PUT'])
def updateUser():
    user = session.get("user")
    if not user:
        return jsonify({"message": "Échec : non connecté"}), 401

    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Échec : requête incomplète ou malformée"}), 400
    except:
        return jsonify({"message": "Échec : requête incomplète ou malformée"}), 400

    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    firstname = data.get("firstname")
    promo = data.get("promo")
    pseudo = data.get("pseudo")

    status = service.user.updateUser(email, password, name, firstname, promo, pseudo, user["id_user"])

    match status:
        case 0:
            return jsonify({"message": "Mise à jour réussie"}), 200
        case 1:
            return jsonify({"message": "Échec : un compte avec cet email existe déjà"}), 409
        case 2:
            return jsonify({"message": "Échec : un compte avec ce pseudo existe déjà"}), 409
        case _:
            return jsonify({"message": "Échec : statut de retour inconnu"}), 500

@user_bp.route("/api/v1/users/password", methods=['PUT'])
def updatePassword():
    user = session.get("user")
    if not user:
        return jsonify({"message": "Échec : non connecté"}), 401

    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Échec : requête incomplète"}), 400
    except:
        return jsonify({"message": "Échec : requête malformée"}), 400

    current_password = data.get("currentPassword")
    new_password = data.get("newPassword")

    if not current_password or not new_password:
        return jsonify({"message": "Échec : requête incomplète"}), 400

    current_user = model.auth.getUserFromEmail(user["email"])
    if not current_user or not crypto.bcrypt.check_password_hash(current_user["password"], current_password):
        return jsonify({"message": "Échec : mot de passe actuel incorrect"}), 401

    status = service.user.updatePassword(new_password, user["id_user"])
    if status == 0:
        return jsonify({"message": "Mot de passe mis à jour"}), 200
    else:
        return jsonify({"message": "Échec : impossible de mettre à jour le mot de passe"}), 500
    
@user_bp.route("/api/v1/users/me", methods=['GET'])
def getCurrentUser():
    user = session.get("user")
    if not user:
        return jsonify({"message": "Non connecté"}), 401
    user_copy = dict(user)
    user_copy.pop("password", None)
    return jsonify(user_copy), 200

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
