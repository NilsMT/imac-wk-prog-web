from flask import Blueprint, request, session, jsonify
import service.admin

admin_bp = Blueprint("admin", __name__)

#get users list
@admin_bp.route("/admin/users", methods=['GET'])
def getUsers():

    #session retrieval
    user = session.get("user")
    if not user:
        return jsonify({"message": "Admin failure : not logged in"}), 401
    if not user.get("admin"):
        return jsonify({"message": "Admin failure : forbidden"}), 403

    users = service.admin.getUsers()
    return jsonify(users), 200

#set user active status
@admin_bp.route("/admin/user/active", methods=['PUT'])
def setActive():
    id_user = active = None

    #session retrieval
    user = session.get("user")
    if not user:
        return jsonify({"message": "Admin failure : not logged in"}), 401
    if not user.get("admin"):
        return jsonify({"message": "Admin failure : forbidden"}), 403

    #form data retrieval
    try:
        id_user = request.form["id_user"]
        active = int(request.form["active"])
    except KeyError:
        return jsonify({"message": "Admin failure : request malformed/incomplete"}), 400
    except ValueError:
        return jsonify({"message": "Admin failure : invalid value for active"}), 400

    status = service.admin.setActive(id_user, active)

    #status handling
    match status:
        case 0:
            return jsonify({"message": "Active status updated successfully"}), 200
        case 1:
            return jsonify({"message": "Admin failure : user not found"}), 404
        case _:
            return jsonify({"message": "Admin failure : unknown returned status"}), 500

#set user admin status
@admin_bp.route("/admin/user/admin", methods=['PUT'])
def setAdmin():
    id_user = admin = None

    #session retrieval
    user = session.get("user")
    if not user:
        return jsonify({"message": "Admin failure : not logged in"}), 401
    if not user.get("admin"):
        return jsonify({"message": "Admin failure : forbidden"}), 403

    #form data retrieval
    try:
        id_user = request.form["id_user"]
        admin = int(request.form["admin"])
    except KeyError:
        return jsonify({"message": "Admin failure : request malformed/incomplete"}), 400
    except ValueError:
        return jsonify({"message": "Admin failure : invalid value for admin"}), 400

    status = service.admin.setAdmin(id_user, admin)

    #status handling
    match status:
        case 0:
            return jsonify({"message": "Admin status updated successfully"}), 200
        case 1:
            return jsonify({"message": "Admin failure : user not found"}), 404
        case _:
            return jsonify({"message": "Admin failure : unknown returned status"}), 500