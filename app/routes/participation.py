from flask import Blueprint, request, session, jsonify
import service.participation

participation_bp = Blueprint("participation", __name__)

#get participation
@participation_bp.route("/api/v1/participations/<int:id_event>", methods=['GET'])
def getParticipation(id_event):
    user = session.get("user")
    if not user:
        return jsonify({"message": "Retrieval failure : not logged in"}), 401

    status, participation = service.participation.getParticipation(user["id_user"], id_event)
    participe = dict(participation[0])
    
    match status:
        case 0:
            return jsonify({"message": "Participation retrieved successfully", "participe": participe["participation_exists"]}), 200
        case _:
            return jsonify({"message": "Retrieval failure : unknown returned status"}), 500

#add participation
@participation_bp.route("/api/v1/participations/<int:id_event>", methods=['POST'])
def addParticipation(id_event):

    user = session.get("user")
    if not user:
        return jsonify({"message": "Participation failure : not logged in"}), 401

    status = service.participation.addParticipation(user["id_user"], id_event)

    match status:
        case 0:
            return jsonify({"message": "Participation added successfully"}), 200
        case 1:
            return jsonify({"message": "Participation failure : already registered"}), 409
        case _:
            return jsonify({"message": "Participation failure : unknown returned status"}), 500

#remove participation
@participation_bp.route("/api/v1/participations/<int:id_event>", methods=['DELETE'])
def removeParticipation(id_event):
    user = session.get("user")
    if not user:
        return jsonify({"message": "Removal failure : not logged in"}), 401

    status = service.participation.removeParticipation(user["id_user"], id_event)

    match status:
        case 0:
            return jsonify({"message": "Participation removed successfully"}), 200
        case 1:
            return jsonify({"message": "Removal failure : participation doesn't exist"}), 404
        case _:
            return jsonify({"message": "Removal failure : unknown returned status"}), 500