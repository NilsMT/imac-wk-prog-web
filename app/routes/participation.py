from flask import Blueprint, request, session, jsonify
import service.participation

participation_bp = Blueprint("participation", __name__)

#add participation
@participation_bp.route("/api/v1/participations", methods=['POST'])
def addParticipation():
    id_event = ""

    #session retrieval
    user = session.get("user")
    if not user:
        return jsonify({"message": "Participation failure : not logged in"}), 401
    
    #form data retrieval
    try:
        id_event = request.form["id_event"]
    except:
        return jsonify({"message": "Participation failure : request malformed/incomplete"}), 400

    status = service.participation.addParticipation(user["id_user"], id_event)

    #status handling
    match status:
        case 0:
            return jsonify({"message": "Participation added successfully"}), 200
        case 1:
            return jsonify({"message": "Participation failure : already registered"}), 409
        case _:
            return jsonify({"message": "Participation failure : unknown returned status"}), 500

#remove participation
@participation_bp.route("/api/v1/participations", methods=['DELETE'])
def removeParticipation():
    id_event = ""

    #session retrieval
    user = session.get("user")
    if not user:
        return jsonify({"message": "Removal failure : not logged in"}), 401

    #form data retrieval
    try:
        id_event = request.form["id_event"]
    except:
        return jsonify({"message": "Removal failure : request malformed/incomplete"}), 400

    status = service.participation.removeParticipation(user["id_user"], id_event)

    #status handling
    match status:
        case 0:
            return jsonify({"message": "Participation removed successfully"}), 200
        case 1:
            return jsonify({"message": "Removal failure : participation doesn't exist"}), 404
        case _:
            return jsonify({"message": "Removal failure : unknown returned status"}), 500