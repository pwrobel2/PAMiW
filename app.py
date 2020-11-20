from flask import Flask, render_template, url_for, request, redirect, make_response, jsonify, session
from dotenv import load_dotenv
from os import getenv
from bcrypt import hashpw, gensalt, checkpw

users = {
    "test": {
        "firstname": "test",
        "lastname": "user",
        "email": "wp@wp.pl",
        "address": "address",
        "password": hashpw("testtest".encode('utf-8'),gensalt(4))
    }
}

load_dotenv()


app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = getenv("SECRET_KEY")


@app.route('/', methods=['GET'])
def index():
    
    return render_template('index.html')


@app.route('/sender/sign-up', methods=['GET'])
def signup_form():
    
    return render_template('signup.html')

@app.route('/sender/sign-up', methods=['POST'])
def signup():

    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    username = request.form.get("login")
    address = request.form.get("address")
    email = request.form.get("email")
    password = request.form.get("password")
    
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

    if username in users:
        return "User already registered", 409

    users[username] = {
        "firstname":firstname,
        "lastname":lastname,
        "email":email,
        "address":address,
        "password":hashpw(password.encode('utf-8'),gensalt(4))
    }

    #flash
    return redirect(url_for('login_form'))


@app.route('/sender/login', methods=['GET'])
def login_form():
    
    return render_template('login.html')

@app.route('/sender/login', methods=['POST'])
def login():
    username = request.form.get("login")
    password = request.form.get("password")

    if username not in users:
        #flash
        return redirect(url_for(login_form))

    pwhash = users[username]["password"]
    if not checkpw(password.encode('utf-8'), pwhash):
        #flash
        return "incorrect password or username", 401
    
    session.clear()
    session[username] = "Logged-in"

    return redirect(url_for('dashboard'))


@app.route('/sender/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/sender/dashboard', methods=['GET'])
def dashboard():
    
    return render_template('workinprogress.html')

@app.route('/sender/users/<username>')
def checkIfAvaliable(username):
    if username in users:
        json = {username:'taken'}
        return jsonify(json)
    else:
        json = {username:'avaliable'}
        return jsonify(json)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)