from flask_app.config.mysqlconnection import connectToMySQL # import the connectToMySQL function from the application.config.mysqlconnection module
from flask import flash
import re

class User: # crear una clase usuario
    def __init__(self, data): 
        self.id_usuario = data["id_usuario"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.edad = data["edad"]
        self.email = data["email"]
        self.apodo = data["apodo"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        
    @staticmethod # método de validación de usuario de formulario de registro
    def validate_user(user):
        is_valid = True
        if len(user["nombre"]) < 2:
            flash("El nombre debe tener desde 2 caracteres", "register")
            is_valid = False
        if len(user["apellido"]) < 2:
            flash("El apellido debe tener desde 2 caracteres", "register")
            is_valid = False
        if len(user["apodo"]) < 2:
            flash("El apodo debe tener desde 2 caracteres", "register")
            is_valid = False
        if len(user["edad"]) < 1:
            flash("La edad debe tener solamente números y desde 1 caracter", "register")
            is_valid = False
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' # validación con regex para email
        if not re.fullmatch(regex, user["email"]):
            flash("El email no es válido", "register")
            is_valid = False
        if len(user["password"]) < 8:
            flash("La contraseña debe tener desde 8 caracteres", "register")
            is_valid = False
        if user["password"] != user["confirm"]:
            flash ("Las contraseñas no coinciden", "register")
            is_valid = False
        return is_valid

    @staticmethod # método de validación de usuario de formulario de login
    def validate_login(user):
        is_valid = True
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' # validación con regex para email
        if not re.fullmatch(regex, user["email"]):
            flash("El email no es válido", "login")
            is_valid = False
        if len(user["password"]) < 8:
            flash("La contraseña debe tener desde 8 caracteres", "login")
            is_valid = False
        return is_valid
        
    
    @classmethod # método para insertar un nuevo usuario en la base de datos
    def save_user(cls, data):
        query = "INSERT INTO usuario (nombre, apellido, edad, email, apodo, password, created_at, updated_at) VALUES (%(nombre)s, %(apellido)s, %(edad)s, %(email)s, %(apodo)s, %(password)s, NOW(), NOW())"
        mysql = connectToMySQL("grupal")
        results = mysql.query_db(query, data)
        user = {"user.id": results}
        return user
    
    @classmethod # metodo para obtener todos los usuarios de la base de datos
    def get_all_users(cls):
        query = "SELECT * FROM usuario"
        mysql = connectToMySQL("grupal")
        results = mysql.query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
            return users
    
    @classmethod # método para obtener un usuario por su id
    def get_user_by_id(cls, id_usuario):
        query = "SELECT * FROM usuario WHERE id = %(id_usuario)s"
        data = {
            'id_usuario': id_usuario
        }
        mysql = connectToMySQL("grupal")
        results = mysql.query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM usuario WHERE email = %(email)s"
        mysql = connectToMySQL("grupal")
        result = mysql.query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None
