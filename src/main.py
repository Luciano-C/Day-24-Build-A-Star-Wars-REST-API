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
from admin import setup_admin
from models import db, User, Characters, Characters_Fav, Planets, Planets_Fav
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200
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


@app.route('/favorite/characters/<int:id>', methods=['POST'])
def add_fav_character(id):
    # Validar si existe personaje
    character = Characters.query.get(id)
    if character:
        check_fav = Characters_Fav.query.filter_by(id_character=id, id_user=1).first()
        if check_fav:
            print(check_fav)
            return "Valor Duplicado"
        else:
            favorite = Characters_Fav()
            favorite.id_character = id
            favorite.id_user = 1
            db.session.add(favorite)
            db.session.commit()
            return "todo ok"
    else:
        return "No existo"

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

@app.route('/favorite/planets/<int:id>', methods=['POST'])
def add_fav_planet(id):
    # Validar si existe planeta
    planet = Planets.query.get(id)
    if planet:
        check_fav = Planets_Fav.query.filter_by(id_planet=id, id_user=1).first()
        if check_fav:
            print(check_fav)
            return "Valor Duplicado"
        else:
            favorite = Planets_Fav()
            favorite.id_planet = id
            favorite.id_user = 1
            db.session.add(favorite)
            db.session.commit()
            return "todo ok"
    else:
        return "No existo"

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
