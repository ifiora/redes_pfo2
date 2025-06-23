from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.hash import sha256_crypt

# Configuramos flask
app = Flask(__name__)
# Seteamos SQLite como base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
# Creamos el objeto auth para autenticación
auth = HTTPBasicAuth()

# Definimos el modelo de la base de datos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    contrasena = db.Column(db.String(200), nullable=False)

# Creamos la base de datos
with app.app_context():
    db.create_all()

# Funcion praa validacion de usuario y contraseña
@auth.verify_password
def verify_password(username, password):
    user = Usuario.query.filter_by(nombre=username).first()
    if user and sha256_crypt.verify(password, user.contrasena):
        return True
    return False

# Endpoint de registro de usuarios
@app.route('/registro', methods=['POST'])
def registro():
    # Obtenemos los datos recibidos de la consulta
    datos = request.get_json()
    # Cargamos el nombre de usuario y contraseña de los datos recibidos
    usuario = datos.get('usuario')
    contrasena = sha256_crypt.hash(datos.get('contraseña'))
    # Validamos si ya existe un usuario con ese nombre
    if Usuario.query.filter_by(nombre=usuario).first():
        return jsonify({"mensaje": "El usuario ya existe"}), 400
    # Creamos el usuario con los datos recibidos
    nuevo_usuario = Usuario(nombre=usuario, contrasena=contrasena)
    # Lo Agregamos a la base de datos
    db.session.add(nuevo_usuario)
    db.session.commit()
    # Devolvemos status code 201 y un mensaje al cliente    
    return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201

# Endpoint de login de usuario
@app.route('/login', methods=['POST'])
def login():
    # Obtenemos los datos de la consulta
    datos = request.get_json()
    # Buscamos en la base de datos el primer usuario con el nombre recibido
    user = Usuario.query.filter_by(nombre=datos.get('usuario')).first()
    # Usamos la biblioteca passlib para verificar si la contraseña es correcta
    if user and sha256_crypt.verify(datos.get('contraseña'), user.contrasena):
        # Si la contraseña es correcta enviamos un mensaje al cliente con estado 200 indicando que el login fue exitoso
        return jsonify({"mensaje": "Login exitoso"}), 200 
    # Si la contraseña es incorrecta devolvemos un estado 401 (Unauthorized) indicando que el login falló
    return jsonify({"mensaje": "Credenciales incorrectas"}), 401

# Endpoint de tareas
@app.route('/tareas', methods=['GET'])
# Indicamos que este endpoint necesita que el usuario este autenticado con la autenticacion basica de Flask
@auth.login_required
def tareas():
    return '''
    <html><body><h1>Bienvenido al gestor de tareas, usuario autenticado</h1></body></html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
