from flask import Blueprint, request, session, jsonify
import service.admin

admin_bp = Blueprint("admin", __name__)

#get users list
@admin_bp.route("/api/v1/admin/users", methods=['GET'])
def getUsers():

    #session retrieval
    user = session.get("user")
    if not user:
        return jsonify({"message": "Admin failure : not logged in"}), 401
    if user["admin"] != 1:
        return jsonify({"message": "Admin failure : forbidden"}), 403

    users = service.admin.getUsers(user["id_user"])
    return jsonify(users), 200

#update user
@admin_bp.route("/api/v1/admin/users/<id_user>", methods=['PUT'])
def updateUser(id_user):
    user = session.get("user")
    if not user:
        return jsonify({"message": "Admin failure : not logged in"}), 401
    if user["admin"] != 1:
        return jsonify({"message": "Admin failure : forbidden"}), 403

    data = request.get_json()
    active = data.get("active")
    admin = data.get("admin")

    if active is None and admin is None:
        return jsonify({"message": "Admin failure : request malformed/incomplete"}), 400

    status = 0
    try:
        if active is not None:
            status = service.admin.setActive(id_user, int(active))
        if admin is not None:
            status = service.admin.setAdmin(id_user, int(admin))
    except ValueError:
        return jsonify({"message": "Admin failure : invalid value"}), 400

    match status:
        case 0:
            return jsonify({"message": "User updated successfully"}), 200
        case 1:
            return jsonify({"message": "Admin failure : user not found"}), 404
        case _:
            return jsonify({"message": "Admin failure : unknown returned status"}), 500