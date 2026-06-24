from flask import Blueprint, request, session, jsonify
import service.event

event_bp = Blueprint("event", __name__)

#create event
@event_bp.route("/event", methods=['POST'])
def createEvent():
    user = session.get("user")
    data_event = request.form

    messsage, status = service.event.createEvent(data_event, user["id_user"])
    return jsonify({"message" : messsage}), status

#delete event
@event_bp.route("/event/<int:id_event>", methods=['DELETE'])
def deleteEvent(id_event):
    user = session.get("user")

    messsage, status = service.event.deleteEvent(id_event, user["id_user"])
    return jsonify({"message" : messsage}), status

#update event
@event_bp.route("/event/<int:id_event>", methods=['PUT'])
def updateEvent(id_event):
    user = session.get("user")
    data_event = request.form

    messsage, status = service.event.updateEvent(data_event, id_event, user["id_user"])
    return jsonify({"message" : messsage}), status

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