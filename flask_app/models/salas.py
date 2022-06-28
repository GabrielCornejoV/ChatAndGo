from flask_app.config.mysqlconnection import connectToMySQL 
from flask import flash
import re

class Sala:
    def __init__(self, data):
        self.id_sala = data["id_sala"]
        self.nombre_sala = data["nombre_sala"]
        self.descripcion = data["descripcion"]
        self.administrador = data["administrador"]
        self.nombre = data["nombre"]
        self.mayor_edad = True if data["mayor_edad"] == 1 else False
        self.id_usuario = data["id_usuario"]

    @staticmethod
    def validar_sala(sala):
        is_valid = True
        if len(sala["nombre_sala"]) < 3:
            flash("El nombre debe tener desde 3 caracteres", "error_sala")
            print("falla nombre")
            is_valid = False
        if len(sala["descripcion"]) < 3:
            flash("La descripción debe tener desde 3 caracteres", "error_sala")
            print("falla descripcion")
            is_valid = False
        return is_valid
    
    @classmethod
    def muestra_salas(cls):
        query = "SELECT * FROM usuario JOIN sala ON usuario.id_usuario = sala.id_usuario"
        mysql = connectToMySQL("grupal")
        results = mysql.query_db(query)
        salas = []
        for sala in results:
            salas.append(cls(sala))
        return salas

    @classmethod
    def crear_sala(cls, data):
        query = "INSERT INTO sala (nombre_sala, descripcion, mayor_edad, created_at, updated_at, id_usuario) VALUES (%(nombre_sala)s, %(descripcion)s, %(mayor_edad)s,  NOW(), NOW() ,%(id_usuario)s)"
        mysql = connectToMySQL("grupal")
        results = mysql.query_db(query, data)
        sala = {"sala.id_sala": results}
        return sala

    @classmethod
    def get_sala_by_id_sala(cls, data):
        query = "SELECT * FROM usuario JOIN sala ON usuario.id_usuario = sala.id_usuario WHERE sala.id_sala = %(id_sala)s"
        #query = "SELECT * FROM sala WHERE id_sala = %(id_sala)s"
        mysql = connectToMySQL("grupal")
        results = mysql.query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def eliminar_sala(cls, data):
        query = "DELETE FROM sala WHERE id_sala = %(id_sala)s"
        mysql = connectToMySQL("grupal")
        results = mysql.query_db(query, data)
        return results
    
    @classmethod
    def update_sala(cls, data):
        query = "UPDATE sala SET nombre_sala = %(nombre_sala)s, descripcion = %(descripcion)s, administrador = %(administrador)s, mayor_edad = %(mayor_edad)s WHERE id_sala = %(id_sala)s"
        mysql = connectToMySQL("grupal")
        results = mysql.query_db(query, data)
        return results


