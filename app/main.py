#############################
#init and imports
#############################
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask
import secrets
import database

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

#############################
#routes
#############################
#https://stackoverflow.com/questions/11994325/how-to-divide-flask-app-into-multiple-py-files

from routes.page import page_bp
from routes.auth import auth_bp
from routes.user import user_bp
from routes.participation import participation_bp
from routes.event import event_bp
from routes.admin import admin_bp
from routes.comment import comment_bp

app.register_blueprint(page_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(participation_bp)
app.register_blueprint(event_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(comment_bp)

#############################
#special behavior
#############################

#on app closure
@app.teardown_appcontext
def on_close(exception):
    database.disconnect_db()