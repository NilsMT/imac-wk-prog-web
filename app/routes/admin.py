from flask import Blueprint, request, session, jsonify
import service.admin

admin_bp = Blueprint("admin", __name__)