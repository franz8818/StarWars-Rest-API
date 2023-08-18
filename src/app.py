"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, People
from models import db, Planet
from models import db, Vehicle

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#PEOPLE
@app.route('/people', methods=['GET'])
def get_all_people():
    all_people = People.query.all()
    if len(all_people) < 1 :  
        return jsonify({"msg": "Not found"}), 404
    results = list(map(lambda item: item.serialize(), all_people))

    return jsonify(results), 200

@app.route('/people/<int:people_uid>', methods=['GET'])
def get_one_people(people_uid):
    people = People.query.get(people_uid)
    if people is None :
        return jsonify({"msg": f'people with uid {people_uid} not found'}), 404
    result = people.serialize()

    return jsonify(result), 200


@app.route('/people', methods=['POST'])
def create_one_people():
    body = json.loads(request.data)
    new_people = People(
        name = body["name"],
        image = body["image"],
        gender = body["gender"],
        birth_year = body["birth_year"],
        height = body["height"],
        mass = body["mass"],
        hair_color = body["hair_color"],
        skin_color = body["skin_color"],
        eye_color = body["eye_color"]
    )
    db.session.add(new_people)
    db.session.commit()
    result = {"msg": "people created succesfully"}
    return jsonify(result), 200

@app.route('/people/<int:people_uid>', methods=['PUT'])
def modify_one_people(people_uid):
    people = People.query.get(people_uid)
    if people is None :
        return jsonify({"msg": f'people with uid {people_uid} not found'}), 404
    body = json.loads(request.data)
    people = People(
        name = body["name"],
        image = body["image"],
        gender = body["gender"],
        birth_year = body["birth_year"],
        height = body["height"],
        mass = body["mass"],
        hair_color = body["hair_color"],
        skin_color = body["skin_color"],
        eye_color = body["eye_color"]
    )
    db.session.commit()
    result = {"msg": "people modify succesfully"}
    return jsonify(result), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)