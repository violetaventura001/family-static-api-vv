"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False #it ignores the last slashes in a URL (if it exsist)
CORS(app) #super important line

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
#GET ALL THE MEMEBER
@app.route('/members', methods=['GET'])
def get_all_members():
    everyone = jackson_family.get_all_members()
    return jsonify(everyone), 200

#GET ONE MEMBER BY ID ASSIGNED
@app.route('/member/<int:id>', methods=['GET'])
def get_one_member(id):
    everyone = jackson_family.get_member(id)
    return jsonify(everyone), 200

#C —> Create—>  Post (Insert Data)
@app.route('/member', methods=['POST'])
def add_member():
    person = request.json
    jackson_family.add_member(person)
    print(person)
    return "", 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
