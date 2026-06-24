from flask import Blueprint, request, session, jsonify
import service.comment

comment_bp = Blueprint("comment", __name__)