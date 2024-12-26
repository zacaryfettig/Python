from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import random
from string import ascii_uppercase
import json
import boto3
import datetime
from datetime import date

#from database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from local_settings import postgresql as settings
import psycopg2


#Initialize Flask App
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Password12@localhost:5432/chatapp"
app.config["SECRET_KEY"] = "%62Sk{0Ii2"
socketio = SocketIO(app)


############login page###############
db = SQLAlchemy(app)

#Database Model
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password_hash = db.Column(db.String(400), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route("/")
def home():
    session.clear()
    if "username" in session :
        return redirect(url_for('room'))
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form['username']
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['username'] = username
        return redirect(url_for('room'))
    else:
        return render_template("index.html")
    
@app.route("/register", methods=["POST"])
def register():
    username = request.form['username']
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("index.html", error="User already exists")
    else:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('room'))

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


###############Chat Config#####################################################################

#room information dictonary
rooms = {}

#Generate Room Code
def generate_unique_code(Length):
    while True:
        code = ""
        for _ in range(Length):
            code += random.choice(ascii_uppercase)

        if code not in rooms: 
            break

        return code
      
room = "Messages"
rooms[room] = {"members": 0, "messages": []}

@app.route("/room")
def room():
    room = "Messages"
    if session.get("username") is None:
        return redirect(url_for("home"))

    return render_template("conformation.html")