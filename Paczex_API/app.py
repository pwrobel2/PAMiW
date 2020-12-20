from flask import Flask, render_template, url_for, request, redirect, make_response, jsonify
from dotenv import load_dotenv
from os import getenv
from redis import StrictRedis
from datetime import datetime
import uuid
from flask_hal import HAL
from flask_hal.document import Document, Embedded
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import re

load_dotenv()



REDIS_URL = getenv("REDIS_URL")


db = StrictRedis.from_url(REDIS_URL)


SESSION_TYPE = 'redis'
SESSION_REDIS = db


app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config['JWT_SECRET_KEY'] = getenv("JWT_SECRET")
app.config['JWT_TOKEN_LOCATION'] = 'headers'

jwt = JWTManager(app)

    
@app.before_request
def test_db():
    try:
        db.ping()
    except:
        return "Error: Can't connect to redis", 500

@app.route('/', methods=['GET'])
def index():
    
    token = create_access_token(identity='duda')
    return jsonify(test_user_jwt = token)




@app.route('/sender/packages', methods=['GET'])
@jwt_required
def dashboard_print():
    user = get_jwt_identity()
    if user is None:
        return jsonify(msg='Unauthorized'),401

    packages = []
    for i in get_packages(user):
        uuid = db.hget(f'package:{i}', "id")
        uuid = uuid.decode()
        name = db.hget(f'package:{i}', "name")
        name = name.decode()
        lockerID = db.hget(f'package:{i}', "lockerID")
        lockerID = lockerID.decode()
        size = db.hget(f'package:{i}', "size")
        size = size.decode()
        status = db.hget(f'package:{i}', "status")
        status = status.decode()
        tmp = {'uuid':uuid,'name':name,'lockerID':lockerID,'size':size,'status':status}
        packages.append(Embedded(data=tmp))
    toJSON = Document(embedded = {'packages':Embedded(data = packages)})
    return toJSON.to_json()

@app.route('/sender/package', methods=['POST'])
@jwt_required
def dashboard_add():
    user = get_jwt_identity()
    if user is None:
        return jsonify(msg='Unauthorized'),401

    name = request.args.get("name")
    lockerID = request.args.get("lockerID")
    size = request.args.get("size")
    if (name != None) or (lockerID != None) or (size != None):
        packageID = add_package(user, name, lockerID, size)
        return jsonify(msg = 'Added package', package_id = packageID),201
    else:
        return jsonify(msg = "No data provided for new package."), 400

@app.route('/sender/package/<packageID>',methods=['DELETE'])
@jwt_required
def delete_package(packageID):
    user = get_jwt_identity()
    if user is None:
        return jsonify(msg='Unauthorized'),401

    if packageID is None:
        return jsonify(msg = 'No package ID provided.'),400

    remove_package(user,packageID)
    return jsonify(msg = 'Package removed', packageID = packageID), 200

@app.route('/sender/package/<packageID>',methods=['PUT'])
@jwt_required
def update_package_status(packageID):
    user = get_jwt_identity()
    if user is None:
        return jsonify(msg='Unauthorized'),401

    pattern = re.compile(r"courier\d+")

    if(db.sismember(f"packages:{user}",packageID)) or (pattern.fullmatch(user)):
        new_status = update_package(packageID)
        return jsonify(msg = 'Package status updated', newStatus = new_status ,packageID = packageID), 200
    else:
        return jsonify(msg = 'Forbidden'),403


def add_package(username, name, lockerID, size):
    tmp = uuid.uuid4()
    packageID = tmp.int
    db.hset(f"package:{packageID}","id", packageID)
    db.hset(f"package:{packageID}","name", name)
    db.hset(f"package:{packageID}","lockerID", lockerID)
    db.hset(f"package:{packageID}","size", size)
    db.hset(f"package:{packageID}","status","Generated")
    db.sadd(f"packages:{username}", packageID)
    return packageID

def remove_package(username, packageID):
    db.srem(f"packages:{username}", packageID)
    db.delete(f"package:{packageID}")
    return True

def update_package(packageID):
    if(db.hexists(f"package:{packageID}","id")):
        status = db.hget(f"package:{packageID}","status").decode()
        if(status == "Generated"):
            db.hset(f"package:{packageID}","status","In transit")
            return "In transit"
        elif(status == "In transit"):
            db.hset(f"package:{packageID}","status","Delivered")
            return "Delivered"
        elif(status == "Delivered"):
            db.hset(f"package:{packageID}","status","Recived")
            return "Recived"
        return status
    else:
        return False

def get_packages(username):
    pattern = re.compile(r"courier\d+")
    if pattern.fullmatch(username):
        keys = db.keys("package:*")
        package_IDs = []
        for key in keys:
            tmp = key.decode().split(":")
            package_IDs.append(tmp[1])
        return package_IDs
    else:
        keys = db.smembers(f"packages:{username}")
        package_IDs = []
        for i in keys:
            tmp = i.decode()
            package_IDs.append(tmp)
        return package_IDs


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)