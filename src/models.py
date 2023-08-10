from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorites = db.relationship('Favorites', backref='user', lazy=True)

    def __repr__(self):
        return f"id: {self.id}, username: {self.username}"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "favorites": list(map(lambda favorite: favorite.serialize(), self.favorites))
        }
    
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    birth_year = db.Column(db.String(64))
    gender = db.Column(db.String(64))
    height = db.Column(db.Integer)
    skin_color = db.Column(db.String(120))
    eye_color = db.Column(db.String(120))
    favorites = db.relationship('Favorites', backref='people', lazy=True)

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    diameter = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    climate = db.Column(db.String(120))
    terrain = db.Column(db.String(120))
    gravity = db.Column(db.String(120))
    favorites = db.relationship('Favorites', backref='planets', lazy=True)

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "orbital_period": self.orbital_period,
            "climate": self.climate,
            "terrain": self.terrain,
            "gravity": self.gravity,
        }
    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planets_id": self.planets_id,
        }