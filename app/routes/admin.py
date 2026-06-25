from flask import Blueprint, request, session, jsonify
import service.admin

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/api/v1/admin/users", methods=['GET'])
def getUsers():
    user = session.get("user")
    if not user:
        return jsonify({"message": "Échec : non connecté"}), 401
    if user["admin"] != 1:
        return jsonify({"message": "Échec : accès interdit"}), 403

    users = service.admin.getUsers(user["id_user"])
    return jsonify(users), 200

@admin_bp.route("/api/v1/admin/users/<id_user>", methods=['PUT'])
def updateUser(id_user):
    user = session.get("user")
    if not user:
        return jsonify({"message": "Échec : non connecté"}), 401
    if user["admin"] != 1:
        return jsonify({"message": "Échec : accès interdit"}), 403

    data = request.get_json()
    active = data.get("active")
    admin = data.get("admin")

    if active is None and admin is None:
        return jsonify({"message": "Échec : requête incomplète ou malformée"}), 400

    status = 0
    try:
        if active is not None:
            status = service.admin.setActive(id_user, int(active))
        if admin is not None:
            status = service.admin.setAdmin(id_user, int(admin))
    except ValueError:
        return jsonify({"message": "Échec : valeur invalide"}), 400

    match status:
        case 0:
            return jsonify({"message": "Utilisateur mis à jour avec succès"}), 200
        case 1:
            return jsonify({"message": "Échec : utilisateur introuvable"}), 404
        case _:
            return jsonify({"message": "Échec : statut de retour inconnu"}), 500
