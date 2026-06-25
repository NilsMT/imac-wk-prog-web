from flask import Blueprint, request, session, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import service.event

event_bp = Blueprint("event", __name__)

UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@event_bp.route("/api/v1/events", methods=['POST'])
def createEvent():
    user = session.get("user")
    data_event = request.form

    image_url = None
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '':
            if not allowed_file(file.filename):
                return jsonify({"message": 'Type de fichier non autorisé (PNG, JPG, JPEG, GIF uniquement).'}), 400
            try:
                filename = secure_filename(file.filename)
                unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
                file.save(filepath)
                image_url = f"/static/uploads/{unique_filename}"
            except Exception as e:
                return jsonify({"message": f"Erreur lors de l'upload de l'image : {str(e)}"}), 500

    message, error = service.event.createEvent(data_event, user["id_user"], image_url)
    if error:
        return jsonify({"message": error}), 400
    return jsonify({"message": message}), 201

@event_bp.route("/api/v1/events/<int:id_event>", methods=['DELETE'])
def deleteEvent(id_event):
    user = session.get("user")
    message, error = service.event.deleteEvent(id_event, user["id_user"])
    if error:
        return jsonify({"message": error}), 400
    return jsonify({"message": message}), 200

@event_bp.route("/api/v1/events/<int:id_event>", methods=['PUT'])
def updateEvent(id_event):
    user = session.get("user")
    data_event = request.form
    message, error = service.event.updateEvent(data_event, id_event, user["id_user"])
    if error:
        return jsonify({"message": error}), 400
    return jsonify({"message": message}), 200

@event_bp.route("/api/v1/events/all", methods=['GET'])
def getAllEvents():
    objects, error = service.event.getAllEvents()
    if error:
        return jsonify({"message": error}), 500
    return jsonify(objects), 200

@event_bp.route("/api/v1/events/allNext", methods=['GET'])
def getAllNextEvents():
    objects, error = service.event.getAllNextEvents()
    if error:
        return jsonify({"message": error}), 500
    return jsonify(objects), 200

@event_bp.route("/api/v1/events/myNext", methods=['GET'])
def getNextEvent():
    user = session.get("user")
    obj, error = service.event.getNextEvent(user["id_user"])
    if error:
        return jsonify({"message": error}), 500
    return jsonify(obj), 200

@event_bp.route("/api/v1/events/myEvents", methods=['GET'])
def getMyEvents():
    user = session.get("user")
    objects, error = service.event.getMyEvents(user["id_user"])
    if error:
        return jsonify({"message": error}), 500
    return jsonify(objects), 200
