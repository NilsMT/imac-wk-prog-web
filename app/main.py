#############################
#init and imports
#############################

import sys, os
#to be able to do service.XXX
sys.path.insert(0, os.path.dirname(__file__))

#import
from flask import Flask, render_template
from flask_bcrypt import Bcrypt
import database

#services
import service.example

app = Flask(__name__)
bcrypt = Bcrypt(app)

#############################
#routes
#############################

#pages
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/example") # exemple avec utilisation de service
def example():
    return render_template("example.html", author = service.example.getAuthors())

#############################
#special behaviors
#############################
@app.teardown_appcontext
def on_close(exception):
    database.disconnect_db()