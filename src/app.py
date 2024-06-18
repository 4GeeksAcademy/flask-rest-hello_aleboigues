# Importamos las dependencias necesarias
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Character_fav, Planet, Planet_fav

# Configuración de la aplicación Flask
app = Flask(__name__)
app.url_map.strict_slashes = False

# Configuración de la base de datos
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de Flask Migrate y la base de datos
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Manejo de errores personalizado para APIException
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generación del sitemap con todos los endpoints disponibles
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Endpoint para listar todos los usuarios
@app.route("/users", methods=['GET'])
def list_users():
    users = User.query.all()
    if not users:
        return jsonify({"msg": "No se han encontrado usuarios"}), 404
    return jsonify([user.serialize() for user in users]), 200

# Endpoint para listar todos los favoritos de un usuario
@app.route("/users/favorites", methods=['GET'])
def list_user_favorites():
    # Para este ejemplo, supondremos que tenemos un usuario actual con id 1
    # Esto debería ser ajustado para manejar la autenticación real
    user_id = 1
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    
    # Obtener todos los favoritos del usuario
    favorite_characters = Character_fav.query.filter_by(user_id=user_id).all()
    favorite_planets = Planet_fav.query.filter_by(user_id=user_id).all()
    
    # Serializar los favoritos
    characters_serialized = [fav.serialize() for fav in favorite_characters]
    planets_serialized = [fav.serialize() for fav in favorite_planets]
    
    return jsonify({
        "favorite_characters": characters_serialized,
        "favorite_planets": planets_serialized
    }), 200

# Endpoint para añadir un nuevo planeta favorito al usuario actual
@app.route("/favorite/planet/<int:planet_id>", methods=['POST'])
def add_planet_favorite(planet_id):
    # Para este ejemplo, supondremos que tenemos un usuario actual con id 1
    # Esto debería ser ajustado para manejar la autenticación real
    user_id = 1
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    
    # Verificar si el planeta existe
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planeta no encontrado"}), 404
    
    # Crear una nueva entrada en la tabla de favoritos de planetas
    new_favorite = Planet_fav(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({"msg": "Planeta añadido a favoritos correctamente"}), 200

# Endpoint para añadir un nuevo personaje favorito al usuario actual
@app.route("/favorite/people/<int:people_id>", methods=['POST'])
def add_character_favorite(people_id):
    # Para este ejemplo, supondremos que tenemos un usuario actual con id 1
    # Esto debería ser ajustado para manejar la autenticación real
    user_id = 1
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    
    # Verificar si el personaje existe
    character = Character.query.get(people_id)
    if not character:
        return jsonify({"msg": "Personaje no encontrado"}), 404
    
    # Crear una nueva entrada en la tabla de favoritos de personajes
    new_favorite = Character_fav(user_id=user_id, character_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({"msg": "Personaje añadido a favoritos correctamente"}), 200

# Endpoint para eliminar un planeta favorito del usuario actual
@app.route("/favorite/planet/<int:planet_id>", methods=['DELETE'])
def delete_planet_favorite(planet_id):
    # Para este ejemplo, supondremos que tenemos un usuario actual con id 1
    # Esto debería ser ajustado para manejar la autenticación real
    user_id = 1
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    
    # Verificar si el planeta favorito existe
    favorite = Planet_fav.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"msg": "Planeta favorito no encontrado"}), 404
    
    # Eliminar la entrada de la tabla de favoritos de planetas
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"msg": "Planeta favorito eliminado correctamente"}), 200

# Endpoint para eliminar un personaje favorito del usuario actual
@app.route("/favorite/people/<int:people_id>", methods=['DELETE'])
def delete_character_favorite(people_id):
    # Para este ejemplo, supondremos que tenemos un usuario actual con id 1
    # Esto debería ser ajustado para manejar la autenticación real
    user_id = 1
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    
    # Verificar si el personaje favorito existe
    favorite = Character_fav.query.filter_by(user_id=user_id, character_id=people_id).first()
    if not favorite:
        return jsonify({"msg": "Personaje favorito no encontrado"}), 404
    
    # Eliminar la entrada de la tabla de favoritos de personajes
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"msg": "Personaje favorito eliminado correctamente"}), 200

# Ejecutar la aplicación si se ejecuta directamente este archivo
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

