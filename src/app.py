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
from models import db, User, Character, Character_fav, Planet, Planet_fav
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
       

#USUARIOS

#traer todos los usuarios
@app.route("/user",methods=['GET']) 
def get_user():
    users=User.query.all()
    resultados=list(map(lambda item:item.serialize(), users))
    if not users:
        return jsonify({"msg":"no se han encontrado usuarios"}), 404
    return jsonify(resultados), 200

#traer un usuario concreto
@app.route("/user/<int:user_id>",methods=['GET']) 
def get_user_by_id(user_id):
    user=User.query.get(user_id) 
    if user is None:
     return jsonify({"msg":"no se han encontrado usuario"}), 404
    return jsonify(user.serialize()), 200

@app.route('/user', methods=['GET'])
def handle_hello():  
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200


#PERSONAJES

#traer todos los personajes
@app.route("/character",methods=['GET']) 
def get_character():
    characters=character.query.all()
    resultados=list(map(lambda item:item.serialize(), characters))
    if not characters:
        return jsonify({"msg":"no se han encontrado personajes"}), 404
    return jsonify(resultados), 200

#traer un personaje concreto
@app.route("/character/<int:character_id>",methods=['GET']) 
def get_character_by_id(character_id):
    character=character.query.get(character_id)
   
    if character is None:
        return jsonify({"msg":"no se han encontrado personaje"}), 404
    return jsonify(character.serialize()), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
