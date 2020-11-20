from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime

app = Flask(__name__)



@app.route('/', methods=['GET','POST'])
def index():
    
    return render_template('index.html')


@app.route('/sender/sign-up', methods=['POST','GET'])
def signup():
    
    return render_template('signup.html')


@app.route('/sender/login', methods=['POST','GET'])
def login():
    
    return render_template('workinprogress.html')

@app.route('/sender/logout', methods=['GET'])
def logout():
    
    return render_template('workinprogress.html')


@app.route('/sender/dashboard', methods=['GET'])
def dashboard():
    
    return render_template('workinprogress.html')


if __name__ == "__main__":
    app.run(debug=True)