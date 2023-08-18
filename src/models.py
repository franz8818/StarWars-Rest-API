from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#estas son las tablas 
#PEOPLE
class People(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    image = db.Column(db.String(250), unique=True, nullable=False)
    gender = db.Column(db.String(6), unique=True, nullable=False)
    birth_year = db.Column(db.String(80), unique=False, nullable=False)
    height = db.Column(db.String(80), unique=False, nullable=False)
    mass = db.Column(db.String(80), unique=False, nullable=False)
    hair_color = db.Column(db.String(80), unique=False, nullable=False)
    skin_color = db.Column(db.String(80), unique=False, nullable=False)
    eye_color = db.Column(db.String(80), unique=False, nullable=False)
    
    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "image": self.image,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            # do not serialize the password, its a security breach
        }
    
    #PLANETS
    class Planets(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    image = db.Column(db.String(250), unique=True, nullable=False)
    population = db.Column(db.String(15), unique=True, nullable=False)
    terrain = db.Column(db.String(80), unique=False, nullable=False)
    climate = db.Column(db.String(80), unique=False, nullable=False)
    surface_water = db.Column(db.String(80), unique=False, nullable=False)
    rotation_period = db.Column(db.String(80), unique=False, nullable=False)
    orbital_period = db.Column(db.String(80), unique=False, nullable=False)
    diameter = db.Column(db.String(80), unique=False, nullable=False)
    
    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "image": self.image,
            "population": self.population,
            "terrain": self.terrain,
            "climate": self.climate,
            "surface_water": self.surface_water,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            # do not serialize the password, its a security breach
        }
    
    #VEHICLES
    class Planets(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    image = db.Column(db.String(250), unique=True, nullable=False)
    model = db.Column(db.String(15), unique=True, nullable=False)
    vehicle_class = db.Column(db.String(80), unique=False, nullable=False)
    manufacturer = db.Column(db.String(80), unique=False, nullable=False)
    cost_in_credits = db.Column(db.String(80), unique=False, nullable=False)
    length = db.Column(db.String(80), unique=False, nullable=False)
    passengers = db.Column(db.String(80), unique=False, nullable=False)
    cargo_capacity = db.Column(db.String(80), unique=False, nullable=False)
    
    def __repr__(self):
        return '<Vehicles %r>' % self.name

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "image": self.image,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "passengers": self.passengers,
            "cargo_capacity": self.cargo_capacity,
            # do not serialize the password, its a security breach
        }