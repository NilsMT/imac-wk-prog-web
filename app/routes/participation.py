from flask import Blueprint, request, session, jsonify
import service.participation

participation_bp = Blueprint("participation", __name__)

@participation_bp.route("/api/v1/participations/<int:id_event>", methods=['GET'])
def getParticipation(id_event):
    user = session.get("user")
    if not user:
        return jsonify({"message": "Échec : non connecté"}), 401

    status, participation = service.participation.getParticipation(user["id_user"], id_event)
    participe = dict(participation[0])

    match status:
        case 0:
            return jsonify({"message": "Participation récupérée avec succès", "participe": participe["participation_exists"]}), 200
        case _:
            return jsonify({"message": "Échec : statut de retour inconnu"}), 500

@participation_bp.route("/api/v1/participations/<int:id_event>", methods=['POST'])
def addParticipation(id_event):
    user = session.get("user")
    if not user:
        return jsonify({"message": "Échec : non connecté"}), 401

    status = service.participation.addParticipation(user["id_user"], id_event)

    match status:
        case 0:
            return jsonify({"message": "Participation ajoutée avec succès"}), 200
        case 1:
            return jsonify({"message": "Échec : vous participez déjà à cet événement"}), 409
        case _:
            return jsonify({"message": "Échec : statut de retour inconnu"}), 500

@participation_bp.route("/api/v1/participations/<int:id_event>", methods=['DELETE'])
def removeParticipation(id_event):
    user = session.get("user")
    if not user:
        return jsonify({"message": "Échec : non connecté"}), 401

    status = service.participation.removeParticipation(user["id_user"], id_event)

    match status:
        case 0:
            return jsonify({"message": "Participation supprimée avec succès"}), 200
        case 1:
            return jsonify({"message": "Échec : participation introuvable"}), 404
        case _:
            return jsonify({"message": "Échec : statut de retour inconnu"}), 500
