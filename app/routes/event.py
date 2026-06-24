from flask import Blueprint, request, session, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import service.event

event_bp = Blueprint("event", __name__)

UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 Mo

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#create event
@event_bp.route("/event", methods=['POST'])
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
                filepath = os.path.join(
                    UPLOAD_FOLDER,
                    unique_filename
                )
                file.save(filepath)
                image_url = f"/static/uploads/{unique_filename}"
            except Exception as e:
                return jsonify({"message": f"Erreur lors de l'upload de l'image : {str(e)}"}), 500

    messsage, status = service.event.createEvent(data_event, user["id_user"], image_url)
    return jsonify({"message" : messsage}), status

#delete event
@event_bp.route("/event/<int:id_event>", methods=['DELETE'])
def deleteEvent(id_event):
    user = session.get("user")

    message, status = service.event.deleteEvent(id_event, user["id_user"])
    return jsonify({"message" : message}), status

#update event
@event_bp.route("/event/<int:id_event>", methods=['PUT'])
def updateEvent(id_event):
    user = session.get("user")
    data_event = request.form

    message, status = service.event.updateEvent(data_event, id_event, user["id_user"])
    return jsonify({"message" : message}), status

# get events
@event_bp.route("/event/all", methods=['GET'])
def getAllEvents():
    objects, status = service.event.getAllEvents()
    match status:
        case 200:
            return jsonify(objects), status
        case _:
            return jsonify(objects), 500

# get upcoming events the user is participating in
@event_bp.route("/event/allNext", methods=['GET'])
def getAllNextEvents():
    objects, status = service.event.getAllNextEvents()
    match status:
        case 200:
            return jsonify(objects), status
        case _:
            return jsonify(objects), 500

# get the next upcoming event the user is participating in
@event_bp.route("/event/myNext", methods=['GET'])
def getNextEvent():
    user = session.get("user")

    objects, status = service.event.getNextEvent(user["id_user"])
    match status:
        case 200:
            return jsonify(objects), status
        case _:
            return jsonify(objects), 500

# get events the user is participating in
@event_bp.route("/event/myEvents", methods=['GET'])
def getMyEvents():
    user = session.get("user")

    objects, status = service.event.getMyEvents(user["id_user"])
    match status:
        case 200:
            return jsonify(objects), status
        case _:
            return jsonify(objects), 500