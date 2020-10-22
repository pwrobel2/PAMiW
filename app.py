from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)



@app.route('/', methods=['POST','GET'])
def index():
    
    return render_template('index.html')


@app.route('/signup', methods=['POST','GET'])
def signup():
    
    return render_template('signup.html')


@app.route('/login', methods=['POST','GET'])
def login():
    
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)