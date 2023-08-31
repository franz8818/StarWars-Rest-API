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
from models import db, User, Favorite, People, Planet, Vehicle

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

#-------------------------------USERS----------------------------------------

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id = user_id).all()
    if len(favorites) < 1 :  
        return jsonify({"msg": "Not found"}), 404
    results = list(map(lambda item: item.serialize(), favorites))

    return jsonify(results), 200

@app.route('/user/<int:user_id>/favorites', methods=['POST'])
def create_one_favorite(user_id):
    body = json.loads(request.data)
    new_favorite = Favorite(
        user_id = user_id,
        people_uid = body["people_uid"] if "people_uid" in body else None,
        planet_uid = body["planet_uid"] if "planet_uid" in body else None,
        vehicle_uid = body["vehicle_uid"] if "vehicle_uid" in body else None
    )
    db.session.add(new_favorite)
    db.session.commit()
    result = {"msg": "favorite created succesfully"}
    return jsonify(result), 200


#-------------------------------PEOPLE----------------------------------------
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
    for key in body:
        for col in people.serialize():
            if key == col and key != "uid":
                setattr(people, col, body[key])
    db.session.commit()
    result = {"msg": "people modify succesfully"}
    return jsonify(result), 200

@app.route('/people/<int:people_uid>', methods=['DELETE'])
def delete_one_people(people_uid):
    people_uid.pop(people_uid)
    return jsonify(people_uid)

#-------------------------------PLANETS----------------------------------------
@app.route('/planet', methods=['GET'])
def get_all_planet():
    all_planet = Planet.query.all()
    if len(all_planet) < 1 :  
        return jsonify({"msg": "Not found"}), 404
    results = list(map(lambda item: item.serialize(), all_planet))

    return jsonify(results), 200

@app.route('/planet/<int:planet_uid>', methods=['GET'])
def get_one_planet(planet_uid):
    planet = Planet.query.get(planet_uid)
    if planet is None :
        return jsonify({"msg": f'planet with uid {planet_uid} not found'}), 404
    result = planet.serialize()

    return jsonify(result), 200


@app.route('/planet', methods=['POST'])
def create_one_planet():
    body = json.loads(request.data)
    new_planet = Planet(
        name = body["name"],
        image = body["image"],
        population = body["population"],
        terrain = body["terrain"],
        climate = body["climate"],
        surface_water = body["surface_water"],
        rotation_period = body["rotation_period"],
        orbital_period = body["orbital_period"],
        diameter = body["diameter"]
    )
    db.session.add(new_planet)
    db.session.commit()
    result = {"msg": "planet created succesfully"}
    return jsonify(result), 200

@app.route('/planet/<int:planet_uid>', methods=['PUT'])
def modify_one_planet(planet_uid):
    planet = Planet.query.get(planet_uid)
    if planet is None :
        return jsonify({"msg": f'planet with uid {planet_uid} not found'}), 404
    body = json.loads(request.data)
    for key in body:
        for col in planet.serialize():
            if key == col and key != "uid":
                setattr(planet, col, body[key])
    db.session.commit()
    result = {"msg": "planet modify succesfully"}
    return jsonify(result), 200

#-------------------------------VEHICLES----------------------------------------
@app.route('/vehicle', methods=['GET'])
def get_all_vehicle():
    all_vehicle = Vehicle.query.all()
    if len(all_vehicle) < 1 :  
        return jsonify({"msg": "Not found"}), 404
    results = list(map(lambda item: item.serialize(), all_vehicle))

    return jsonify(results), 200

@app.route('/vehicle/<int:vehicle_uid>', methods=['GET'])
def get_one_vehicle(vehicle_uid):
    vehicle = Vehicle.query.get(vehicle_uid)
    if vehicle is None :
        return jsonify({"msg": f'vehicle with uid {vehicle_uid} not found'}), 404
    result = vehicle.serialize()

    return jsonify(result), 200


@app.route('/vehicle', methods=['POST'])
def create_one_vehicle():
    body = json.loads(request.data)
    new_vehicle = Vehicle(
        name = body["name"],
        image = body["image"],
        model = body["model"],
        vehicle_class = body["vehicle_class"],
        manufacturer = body["manufacturer"],
        cost_in_credits = body["cost_in_credits"],
        length = body["length"],
        passengers = body["passengers"],
        cargo_capacity = body["cargo_capacity"]
    )
    db.session.add(new_vehicle)
    db.session.commit()
    result = {"msg": "vehicle created succesfully"}
    return jsonify(result), 200

@app.route('/vehicle/<int:vehicle_uid>', methods=['PUT'])
def modify_one_vehicle(vehicle_uid):
    vehicle = Vehicle.query.get(vehicle_uid)
    if vehicle is None :
        return jsonify({"msg": f'vehicle with uid {vehicle_uid} not found'}), 404
    body = json.loads(request.data)
    for key in body:
        for col in vehicle.serialize():
            if key == col and key != "uid":
                setattr(vehicle, col, body[key])
    db.session.commit()
    result = {"msg": "vehicle modify succesfully"}
    return jsonify(result), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)