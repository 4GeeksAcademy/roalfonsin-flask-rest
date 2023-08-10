"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorites
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

@app.route('/user', methods=['GET'])
def handle_user():
   
    all_users_query = User.query.all()
    if len(list(all_users_query)) == 0:
        raise APIException('We have no users', 400)
    
    response_body = [repr(user) for user in all_users_query]
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def handle_one_user(user_id):
   
    user_query = User.query.filter_by(id = user_id)
    if len(list(user_query)) == 0:
        raise APIException('User not found', 400)
   
    response_body = user_query[0].serialize()
    return jsonify(response_body), 200

@app.route('/user/<int:current_user_id>/favorites', methods=['GET'])
def handle_favorites(current_user_id):
  
    favorites_query = Favorites.query.filter_by(user_id = current_user_id)
    if len(list(favorites_query)) == 0:
        raise APIException('This user has no favorites or user does not exist', 400)
   
    response_body = [favorite.serialize() for favorite in favorites_query]
    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def handle_people():
    
    all_people_query = People.query.all()
    if len(list(all_people_query)) == 0:
        raise APIException('We have no people', 400)
   
    response_body = [repr(person) for person in all_people_query]
    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def handle_person(people_id):
   
    person_query = People.query.filter_by(id = people_id)
    if len(list(person_query)) == 0:
        raise APIException('Person not found', 400)
    
    response_body = person_query[0].serialize()
    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def handle_planets():
   
    all_planets_query = Planets.query.all()
    if len(list(all_planets_query)) == 0:
        raise APIException('We have no planets', 400)
   
    response_body = [repr(planet) for planet in all_planets_query]
    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_planet(planet_id):
    
    planet_query = Planets.query.filter_by(id = planet_id)
    if len(list(planet_query)) == 0:
        raise APIException('Planet not found', 400)
    
    response_body = planet_query[0].serialize()
    return jsonify(response_body), 200

@app.route('/user/<int:current_user_id>/favorites/people/<int:fav_people_id>', methods=['POST'])
def handle_add_favorite_people(current_user_id, fav_people_id):
    
    user_query = User.query.filter_by(id = current_user_id)
    if len(list(user_query)) == 0:
        raise APIException('User not found', 400)
    
    person_query = People.query.filter_by(id = fav_people_id)
    if len(list(person_query)) == 0:
        raise APIException('Person not found', 400)
    
    favorite_query = Favorites.query.filter_by(user_id = current_user_id, people_id = fav_people_id)
    if len(list(favorite_query)) != 0:
        raise APIException('Favorite already exist', 400)
    
    new_favorite = Favorites(user_id = current_user_id, people_id = fav_people_id, planets_id = None)
    db.session.add(new_favorite)
    db.session.commit()
    response_body = "favorite added"
    return jsonify(response_body), 200

@app.route('/user/<int:current_user_id>/favorites/planets/<int:fav_planet_id>', methods=['POST'])
def handle_add_favorite_planet(current_user_id, fav_planet_id):
    
    user_query = User.query.filter_by(id = current_user_id)
    if len(list(user_query)) == 0:
        raise APIException('User not found', 400)
    
    planet_query = Planets.query.filter_by(id = fav_planet_id)
    if len(list(planet_query)) == 0:
        raise APIException('Planet not found', 400)
    
    favorite_query = Favorites.query.filter_by(user_id = current_user_id, planets_id = fav_planet_id)
    if len(list(favorite_query)) != 0:
        raise APIException('Favorite already exist', 400)
    
    new_favorite = Favorites(user_id = current_user_id, planets_id = fav_planet_id, people_id = None)
    db.session.add(new_favorite)
    db.session.commit()
    response_body = "favorite added"
    return jsonify(response_body), 200

@app.route('/user/<int:current_user_id>/favorites/people/<int:fav_people_id>', methods=['DELETE'])
def handle_delete_favorite_people(current_user_id, fav_people_id):
      
    favorite_query = Favorites.query.filter_by(user_id = current_user_id, people_id = fav_people_id)
    if len(list(favorite_query)) == 0:
        raise APIException('Favorite does not exist', 400)
    
    favorite_to_delete = favorite_query[0]
    db.session.delete(favorite_to_delete)
    db.session.commit()
    response_body = "favorite deleted"
    return jsonify(response_body), 200

@app.route('/user/<int:current_user_id>/favorites/planets/<int:fav_planet_id>', methods=['DELETE'])
def handle_delete_favorite_planet(current_user_id, fav_planet_id):
      
    favorite_query = Favorites.query.filter_by(user_id = current_user_id, planets_id = fav_planet_id)
    if len(list(favorite_query)) == 0:
        raise APIException('Favorite does not exist', 400)
    
    favorite_to_delete = favorite_query[0]
    db.session.delete(favorite_to_delete)
    db.session.commit()
    response_body = "favorite deleted"
    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
