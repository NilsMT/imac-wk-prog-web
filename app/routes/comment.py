from flask import Blueprint, request, session, jsonify
import service.comment
from utils import getCurrentTime

comment_bp = Blueprint("comment", __name__)

@comment_bp.route("/comment/get", methods=['GET'])
def getCommentsOnEvent():
    id_event = ""

    #form data retrieval
    try:
        id_event = request.args.get("id_event")
    except:
        return jsonify({"message" : "Comment retrieval failure : request malformed/incomplete"}),400
    
    comments = service.comment.getCommentsOnEvent(id_event)
    return jsonify(comments),200
           

@comment_bp.route("/comment/add", methods=['POST'])
def addComment():
    id_event = message = ""
    comment_time = getCurrentTime()

    #session retrieval
    user = session.get("user")
    if not user:
        return jsonify({"message": "Comment failure : not logged in"}), 401
    
    #form data retrieval
    try:
        id_event = request.form["id_event"]
        message = request.form["message"]
    except:
        return jsonify({"message" : "Comment failure : request malformed/incomplete"}),400
    
    status = service.comment.addComment(user["id_user"],id_event,message,comment_time)

    #status handling
    match status:
        case 0:
            return jsonify({"message" : "Comment success"}),200
        case 1:
            return jsonify({"message" : "Comment failure"}),500
        case _:
            return jsonify({"message" : "Comment failure : unknown returned status"}),500