# Importación de módulos necesarios
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_marshmallow import Marshmallow
from sqlalchemy.exc import IntegrityError
import datetime

#Creacion de APP Flask
app = Flask(__name__)
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend

# configuro la base de datos, con el nombre el usuario y la clave
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user:password@localhost/test'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/proyecto'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow

#Definimo el modelo de datos
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    categoria= db.Column(db.String(100))
    precio= db.Column(db.String(16))
    stock= db.Column(db.String(20))
    
    def __init__(self,nombre,categoria,precio,stock):
        self.nombre = nombre
        self.categoria =categoria
        self.precio = precio
        self.stock = stock

#Definimos el esquema
class ProductoSchema(ma.Schema):
    class Meta:
        fields = ('id','nombre','categoria', 'precio', 'stock')


#Crear esquemas para la db
producto_schema = ProductoSchema() #trae un producto
productos_schema = ProductoSchema(many=True) #Para traer más de un producto

#Creamos la tablas
with app.app_context():
    db.create_all()

#Endpoint Get
@app.route('/productos', methods=['GET'])
def get_all_productos():
    try:
        productos = Producto.query.all()
        if productos:
            return productos_schema.jsonify(productos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Endpoint Get by Id
@app.route('/productos/<id>', methods=['GET'])
def get_producto(id):
    try:
        producto = Producto.query.get(id)

        if producto:
            return producto_schema.jsonify(producto)
        else:
            return jsonify({'error': 'Producto no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para crear un nuevo producto mediante una solicitud POST
@app.route('/productos', methods=['POST'])
def create_producto():
    try:
        json_data = request.get_json()
        nombre = json_data['nombre']
        categoria = json_data['categoria']
        precio = json_data['precio']
        stock = json_data['stock']
        
        # Cargar datos JSON en un objeto producto
        nuevo_producto = Producto(nombre, categoria, precio, stock)

        # Realizar validaciones adicionales si es necesario

        db.session.add(nuevo_producto)
        db.session.commit()

        return producto_schema.jsonify(nuevo_producto), 201  # Devolver el producto creado con el código 201 (creado)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400  # Devolver mensajes de error de validación con el código 400 (error de solicitud)

# Ruta para actualizar un producto mediante una solicitud PUT
@app.route('/productos/<id>', methods=['PUT'])
def update_producto(id):
    try:
        producto = Producto.query.get(id)

        # Verificar si el producto existe en la base de datos
        if producto:
            json_data = request.get_json()
            producto.nombre = json_data.get('nombre', producto.nombre)
            producto.categoria = json_data.get('categoria', producto.categoria)
            producto.precio = json_data.get('precio', producto.precio)
            producto.stock = json_data.get('stock', producto.stock)
            

            # Realizar validaciones según tus requerimientos

            db.session.commit()
            return producto_schema.jsonify(producto)
        else:
            return jsonify({'error': 'Producto no encontrado'}), 404  # Devolver código 404 si el producto no existe

    except ValidationError as err:
        return jsonify({'error': err.messages}), 400  # Devolver mensajes de error de validación con el código 400 (error de solicitud)

# Ruta para eliminar un producto mediante una solicitud DELETE
@app.route('/productos/<id>', methods=['DELETE'])
def delete_producto(id):
    try:
        producto = Producto.query.get(id)

        # Verificar si el producto existe en la base de datos
        if producto:
            db.session.delete(producto)
            db.session.commit()
            return producto_schema.jsonify(producto)
        else:
            return jsonify({'error': 'Producto no encontrado'}), 404  # Devolver código 404 si el producto no existe

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Devolver código 500 si hay un error durante la eliminación


if __name__ == '__main__':
    app.run(debug=True)