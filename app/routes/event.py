from flask import Blueprint, request, session, jsonify
import service.event

event_bp = Blueprint("event", __name__)

@event_bp.route("/event", methods=['POST'])
def createEvent():
    user = session.get("user")
    message, status = service.event.createEvent(request.form, user["id_user"])
    return jsonify({"message": message}), status

@event_bp.route("/event/<int:id_event>", methods=['DELETE'])
def deleteEvent(id_event):
    user = session.get("user")
    message, status = service.event.deleteEvent(id_event, user["id_user"])
    return jsonify({"message": message}), status

@event_bp.route("/event/<int:id_event>", methods=['PUT'])
def updateEvent(id_event):
    user = session.get("user")
    message, status = service.event.updateEvent(request.form, id_event, user["id_user"])
    return jsonify({"message": message}), status

@event_bp.route("/event/all", methods=['GET'])
def getAllEvents():
    objects, status = service.event.getAllEvents()
    return jsonify(objects), status if status == 200 else 500

@event_bp.route("/event/allNext", methods=['GET'])
def getAllNextEvents():
    objects, status = service.event.getAllNextEvents()
    return jsonify(objects), status if status == 200 else 500

@event_bp.route("/event/myNext", methods=['GET'])
def getNextEvent():
    user = session.get("user")
    objects, status = service.event.getNextEvent(user["id_user"])
    return jsonify(objects), status if status == 200 else 500

@event_bp.route("/event/myEvents", methods=['GET'])
def getMyEvents():
    user = session.get("user")
    objects, status = service.event.getMyEvents(user["id_user"])
    return jsonify(objects), status if status == 200 else 500