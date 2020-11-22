from flask import Flask, render_template, url_for, request, redirect, make_response, jsonify, session, flash
from flask_session import Session
from dotenv import load_dotenv
from os import getenv
from bcrypt import hashpw, gensalt, checkpw
from redis import StrictRedis
from datetime import datetime
import uuid

db = StrictRedis(host='redis',port=6379, db=0)


load_dotenv()
SESSION_TYPE = 'redis'
SESSION_REDIS = db


app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = getenv("SECRET_KEY")
ses = Session(app)

class Label:
    def __init__(self, uuid, name, lockerID, size):
        self.uuid = uuid
        self.name = name
        self.lockerID = lockerID
        self.size = size
    


@app.route('/', methods=['GET'])
def index():
    
    return render_template('index.html')


@app.route('/sender/sign-up', methods=['GET'])
def signup_form():
    
    user = session.get("username")
    if user is not None:
        flash("You are already logged in!")
        return redirect(url_for("dashboard_print"))
    
    return render_template('signup.html')

@app.route('/sender/sign-up', methods=['POST'])
def signup():

    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    username = request.form.get("login")
    address = request.form.get("address")
    email = request.form.get("email")
    password = request.form.get("password")
    password2 = request.form.get("passwordRepeat")
    
    if firstname is None:
        return "No firstname provided", 400
    if lastname is None:
        return "No lastname provided", 400
    if username is None:
        return "No username provided", 400
    if email is None:
        return "No email provided", 400
    if address is None:
        return "No address provided", 400
    if password is None:
        return "No password provided", 400

    if password != password2:
        return "Passwords doesn't match", 409

    if is_user(username):
        return "User already registered", 409


    add_user(username, password, firstname, lastname, email, address)

    #flash successful login
    return redirect(url_for('login_form'))


@app.route('/sender/login', methods=['GET'])
def login_form():

    user = session.get("username")
    if user is not None:
        flash("You are already logged in!")
        return redirect(url_for("dashboard_print"))
    
    return render_template('login.html')

@app.route('/sender/login', methods=['POST'])
def login():
    username = request.form.get("login")
    password = request.form.get("password")

    if not is_login_correct(username, password):
        #flash wrong username password
        return redirect(url_for('login_form'))

    
    session.clear()
    session["start_time"] = datetime.utcnow()
    session["username"] = username
    

    return redirect(url_for('dashboard_print'))


@app.route('/sender/logout', methods=['GET'])
def logout():
    user = session.get("username")
    if user is None:
        flash("Login in first!")
        return redirect(url_for("login_form"))
    session.clear()
    return redirect(url_for('index'))


@app.route('/sender/dashboard', methods=['GET'])
def dashboard_print():
    user = session.get("username")
    if user is None:
        flash("Login in first!")
        return redirect(url_for("login_form"))

    labels = []
    for i in get_labels(user):
        uuid = i
        name = db.hget(f'package:{i}', "name")
        lockerID = db.hget(f'package:{i}', "lockerID")
        size = db.hget(f'package:{i}', "size")
        labels.append(Label(uuid,name,lockerID,size)) 

    return render_template('dashboard.html', labels=labels)

@app.route('/sender/dashboard', methods=['POST'])
def dashboard_add():
    user = session.get("username")
    if user is None:
        flash("Login in first!")
        return redirect(url_for("login_form"))

    name = request.form.get("name")
    lockerID = request.form.get("lockerID")
    size = request.form.get("size")
    add_label(user, name, lockerID, size)

    return redirect(url_for("dashboard_print"))


@app.route('/sender/users/<username>')
def checkIfAvaliable(username):
    if is_user(username):
        json = {username:'taken'}
        return jsonify(json)
    else:
        json = {username:'avaliable'}
        return jsonify(json)


def is_user(username):
    return db.hexists(f"user:{username}", "password")

def is_login_correct(username, password):
    hashed = db.hget(f"user:{username}", "password")
    if not hashed:
        print(f"No password for {username}")
        return False
    
    return checkpw(password.encode(),hashed)

def add_user(username, password, firstname, lastname, email, address):
    hashed = hashpw(password.encode(), gensalt(5))
    db.hset(f"user:{username}","password", hashed)
    db.hset(f"user:{username}","firstname", firstname)
    db.hset(f"user:{username}","lastname", lastname)
    db.hset(f"user:{username}","email", email)
    db.hset(f"user:{username}","address", address)
    return True

def add_label(username, name, lockerID, size):
    pid = str(uuid.uuid4())
    db.hset(f"package:{pid}","name", name)
    db.hset(f"package:{pid}","lockerID", lockerID)
    db.hset(f"package:{pid}","size", size)
    db.sadd(f"packages:{username}", pid)
    return True

def remove_label(username, pid):
    db.srem(f"packages:{username}", pid)
    db.delete(f"package:{pid}")
    return True

def get_labels(username):
    return db.smembers(f"packages:{username}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)