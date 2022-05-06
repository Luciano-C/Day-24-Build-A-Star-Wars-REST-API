"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
# Evita errores de traspaso de información
from flask_cors import CORS
# Importado de utils.py, permiten ver html
from utils import APIException, generate_sitemap
from functions import get_user_favorites
from admin import setup_admin
from models import db, User, Characters, Characters_Fav, Planets, Planets_Fav, Ships, Ships_Fav
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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



# USERS

@app.route('/users', methods=["GET"])
def get_users():
    all_users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users))
    return jsonify(all_users), 200



@app.route('/user/<int:uid>/favorites', methods=["GET"])
def get_favorites(uid):
    # get_user_favorites: función definida en src/functions.py
    favorite_characters = get_user_favorites(uid, Characters_Fav, "id_character", Characters)
    favorite_planets = get_user_favorites(uid, Planets_Fav, "id_planet", Planets)
    favorite_ships = get_user_favorites(uid, Ships_Fav, "id_ship", Ships)
    
    result = [{"characters": favorite_characters}, {"planets": favorite_planets}, {"ships": favorite_ships}]
    return jsonify(result)


# CHARACTERS
@app.route('/characters', methods=["GET"])
def get_characters():
    all_characters = Characters.query.all()
    all_characters = list(map(lambda x: x.serialize(), all_characters))
    print(all_characters)
    return jsonify(all_characters), 200


@app.route('/characters/<int:id>', methods=['GET'])
def get_character(id):
    character = Characters.query.get(id)
    return jsonify(character.serialize()), 200


@app.route('/user/<int:uid>/favorites/characters/<int:id>', methods=['POST'])
def add_fav_character(id, uid):
    # Validar si existe personaje
    character = Characters.query.get(id)
    if character:
        check_fav = Characters_Fav.query.filter_by(id_character=id, id_user=uid).first()
        if check_fav:
            print(check_fav)
            return "Valor Duplicado"
        else:
            favorite = Characters_Fav()
            favorite.id_character = id
            favorite.id_user = uid
            db.session.add(favorite)
            db.session.commit()
            return "todo ok"
    else:
        return "No existo"
    
@app.route('/user/<int:uid>/favorites/characters/<int:id>', methods=['DELETE'])
def del_fav_character(id,uid):
    target = Characters_Fav.query.filter_by(id_character=id, id_user=uid).first()
    if target:
        db.session.delete(target)
        db.session.commit()
        return "Todo ok"
    else:
        return "Character is not favorite"



# PLANETS
@app.route('/planets', methods=["GET"])
def get_planets():
    all_planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))
    return jsonify(all_planets), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    planet = Planets.query.get(id)
    return jsonify(planet.serialize()), 200

@app.route('/user/<int:uid>/favorites/planets/<int:id>', methods=['POST'])
def add_fav_planet(id, uid):
    # Validar si existe planeta
    planet = Planets.query.get(id)
    if planet:
        check_fav = Planets_Fav.query.filter_by(id_planet=id, id_user=uid).first()
        if check_fav:
            print(check_fav)
            return "Valor Duplicado"
        else:
            favorite = Planets_Fav()
            favorite.id_planet = id
            favorite.id_user = uid
            db.session.add(favorite)
            db.session.commit()
            return "todo ok"
    else:
        return "No existo"

@app.route('/user/<int:uid>/favorites/planets/<int:id>', methods=['DELETE'])
def del_fav_planet(id,uid):
    target = Planets_Fav.query.filter_by(id_planet=id, id_user=uid).first()
    if target:
        db.session.delete(target)
        db.session.commit()
        return "Todo ok"
    else:
        return "Planet is not favorite"


# SHIPS
@app.route('/ships', methods=["GET"])
def get_ships():
    all_ships = Ships.query.all()
    all_ships = list(map(lambda x: x.serialize(), all_ships))
    return jsonify(all_ships), 200

@app.route('/ships/<int:id>', methods=['GET'])
def get_ship(id):
    ship = Ships.query.get(id)
    return jsonify(ship.serialize()), 200



@app.route('/user/<int:uid>/favorites/ships/<int:id>', methods=['POST'])
def add_fav_ship(id, uid):
    # Validar si existe nave
    ship = Ships.query.get(id)
    if ship:
        check_fav = Ships_Fav.query.filter_by(id_ship=id, id_user=uid).first()
        if check_fav:
            print(check_fav)
            return "Valor Duplicado"
        else:
            favorite = Ships_Fav()
            favorite.id_ship = id
            favorite.id_user = uid
            db.session.add(favorite)
            db.session.commit()
            return "todo ok"
    else:
        return "No existo"

@app.route('/user/<int:uid>/favorites/ships/<int:id>', methods=['DELETE'])
def del_fav_ship(id,uid):
    target = Ships_Fav.query.filter_by(id_ship=id, id_user=uid).first()
    if target:
        db.session.delete(target)
        db.session.commit()
        return "Todo ok"
    else:
        return "Ship is not favorite"


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
