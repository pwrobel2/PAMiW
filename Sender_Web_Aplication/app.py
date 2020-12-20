from flask import Flask, render_template, url_for, request, redirect, make_response, jsonify, session, flash
from flask_session import Session
from dotenv import load_dotenv
from os import getenv
from bcrypt import hashpw, gensalt, checkpw
from redis import StrictRedis
from datetime import datetime
import uuid
import requests
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, decode_token

load_dotenv()



REDIS_URL = getenv("REDIS_URL")

db = StrictRedis.from_url(REDIS_URL)
SESSION_TYPE = 'redis'
SESSION_REDIS = db
api_url = 'https://paczex-api.herokuapp.com'


app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config['SESSION_COOKIE_SECURE'] = True
app.config['JWT_SECRET_KEY'] = getenv("JWT_SECRET")
app.config['JWT_TOKEN_LOCATION'] = 'headers'

jwt = JWTManager(app)
ses = Session(app)

class Package:
    def __init__(self, uuid, name, lockerID, size):
        self.uuid = uuid
        self.name = name
        self.lockerID = lockerID
        self.size = size
    
@app.before_request
def test_db():
    try:
        db.ping()
    except:
        return "Error: Can't connect to redis", 500

@app.route('/', methods=['GET'])
def index():
    
    return render_template('index.html')


@app.route('/sender/sign-up', methods=['GET'])
def signup_form():
    
    user = session.get("username")
    if user is not None:
        flash("You already logged in!")
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

    flash("Registered successfully!")
    return redirect(url_for('login_form'))


@app.route('/sender/login', methods=['GET'])
def login_form():

    user = session.get("username")
    if user is not None:
        flash("You already logged in!")
        return redirect(url_for("dashboard_print"))
    
    return render_template('login.html')

@app.route('/sender/login', methods=['POST'])
def login():
    username = request.form.get("login")
    password = request.form.get("password")

    if not is_login_correct(username, password):
        flash("Wrong username or password!")
        return redirect(url_for('login_form'))

    
    session.clear()
    session["start_time"] = datetime.utcnow()
    session["username"] = username
    

    return redirect(url_for('dashboard_print'))


@app.route('/sender/logout', methods=['GET'])
def logout():
    user = session.get("username")
    if user is None:
        flash("Log in first!")
        return redirect(url_for("login_form"))
    session.clear()
    return redirect(url_for('index'))


@app.route('/sender/dashboard', methods=['GET'])
def dashboard_print():
    user = session.get("username")
    if user is None:
        flash("Log in first!")
        return redirect(url_for("login_form"))

    token = create_access_token(identity=user)
    auth_header = {"Authorization":f"Bearer {token}"}
    try:
        tmp = requests.get(api_url+'/sender/packages', headers=auth_header).json()
    except:
        return "Couldn't connect to API", 503
    packages = tmp['_embedded']['packages']
    return render_template('dashboard.html', packages = packages)

@app.route('/sender/dashboard', methods=['POST'])
def dashboard_add():
    user = session.get("username")
    if user is None:
        flash("Log in first!")
        return redirect(url_for("login_form"))

    name = request.form.get("name")
    lockerID = request.form.get("lockerID")
    size = request.form.get("size")
    if (size is None) or (lockerID is None) or (name is None):
        return "Not enough package info provided", 400
    
    token = create_access_token(identity=user)
    auth_header = {"Authorization":f"Bearer {token}"}
    try:
        requests.post(api_url+f'/sender/package?name={name}&size={size}&lockerID={lockerID}', headers=auth_header)
        flash(f'Added package: {name}')
    except:
        return "Couldn't connect to API", 503

    return redirect(url_for("dashboard_print"))

@app.route('/sender/package/delete/<packageID>', methods=['GET']) #html form doesn't support delete
def delete_package(packageID):
    user = session.get("username")
    if user is None:
        flash("Log in first!")
        return redirect(url_for("login_form"))

    token = create_access_token(identity=user)
    auth_header = {"Authorization":f"Bearer {token}"}
    try:
        tmp = requests.delete(api_url+f'/sender/package/{packageID}', headers=auth_header)
        flash(f'Deleted package: {packageID}')
    except:
        return "Couldn't connect to API", 503


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)