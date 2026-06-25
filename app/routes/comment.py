from flask import Blueprint, request, session, jsonify
import service.comment
from utils import getCurrentTime

comment_bp = Blueprint("comment", __name__)

@comment_bp.route("/api/v1/comments/<int:id_event>", methods=['GET'])
def getCommentsOnEvent(id_event):
    comments = service.comment.getCommentsOnEvent(id_event)
    return jsonify([dict(comment) for comment in comments]), 200

@comment_bp.route("/api/v1/comments/<int:id_event>", methods=['POST'])
def addComment(id_event):
    comment_time = getCurrentTime()

    user = session.get("user")
    if not user:
        return jsonify({"message": "Échec : non connecté"}), 401

    try:
        message = request.form["message"]
    except:
        return jsonify({"message": "Échec : requête incomplète ou malformée"}), 400

    status = service.comment.addComment(user["id_user"], id_event, message, comment_time)

    match status:
        case 0:
            return jsonify({"message": "Commentaire ajouté avec succès"}), 200
        case 1:
            return jsonify({"message": "Échec de l'ajout du commentaire"}), 500
        case _:
            return jsonify({"message": "Échec : statut de retour inconnu"}), 500
