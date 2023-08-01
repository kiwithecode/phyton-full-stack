from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import ObjectId

# Instantiation
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/factura'
mongo = PyMongo(app)

# Settings
CORS(app)

# Database
db_users = mongo.db.users
db_inventarios = mongo.db.inventarios

# Routes---- usuarios
@app.route('/users', methods=['POST'])
def createUser():
    data = request.json
    id = db_users.insert_one({
        'name': data['name'],
        'email': data['email'],
        'telefono': data['telefono']
    })
    return jsonify({"_id": str(id.inserted_id)})

@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    for doc in db_users.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': doc['email'],
            'telefono': doc['telefono']
        })
    return jsonify(users)

@app.route('/users/<id>', methods=['GET'])
def getUser(id):
  user = db_users.find_one({'_id': ObjectId(id)})
  return jsonify({
      '_id': str(ObjectId(user['_id'])),
      'name': user['name'],
      'email': user['email'],
      'telefono': user['telefono']
  })

@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
  db_users.delete_one({'_id': ObjectId(id)})
  return jsonify({'message': 'User Deleted'})

@app.route('/users/<id>', methods=['PUT'])
def updateUser(id):
  db_users.update_one({'_id': ObjectId(id)}, {"$set": {
    'name': request.json['name'],
    'email': request.json['email'],
    'telefono': request.json['telefono']
  }})
  return jsonify({'message': 'User Updated'})

# Ruta ----- inventario
@app.route('/inventarios', methods=['POST'])
def createInventario():
    data = request.json
    precio = float(data['precio'])
    cantidad = int(data['cantidad'])
    codigo = data['codigo']
    iva = 0.12
    valor_sin_iva = precio * cantidad
    iva = valor_sin_iva * iva
    valor_con_iva = valor_sin_iva + iva

    id = db_inventarios.insert_one({
        'producto': data['producto'],
        'precio': precio,
        'cantidad': cantidad,
        'codigo' : codigo,
        'iva': iva,
        'valor': valor_con_iva,
    })
    return jsonify({"_id": str(id.inserted_id)})

@app.route('/inventarios', methods=['GET'])
def getInventarios():
    inventarios = []
    for doc in db_inventarios.find():
        inventarios.append({
            '_id': str(ObjectId(doc['_id'])),
            'producto': doc['producto'],
            'precio': doc['precio'],
            'cantidad': doc['cantidad'],
            'codigo' : doc['codigo'],
            'iva': doc['iva'],
            'valor': doc['valor']
        })
    return jsonify(inventarios)

@app.route('/inventarios/<id>', methods=['GET'])
def getInventario(id):
    inventario = db_inventarios.find_one({'_id': ObjectId(id)})
    return jsonify({
        '_id': str(ObjectId(inventario['_id'])),
        'producto': inventario['producto'],
        'precio': inventario['precio'],
        'cantidad': inventario['cantidad'],
        'codigo' : inventario['codigo'],
        'iva': inventario['iva'],
        'valor': inventario['valor']
    })

@app.route('/inventarios/<id>', methods=['DELETE'])
def deleteInventario(id):
    db_inventarios.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': 'Inventario Deleted'})

# @app.route('/inventarios/<id>', methods=['PUT'])
# def updateInventario(id):
#     data = request.json
#     precio = float(data['precio'])
#     cantidad = int(data['cantidad'])
#     iva= 0.12

#     iva = precio * cantidad * iva
#     valor_con_iva = precio * cantidad * (1 + iva)

#     db_inventarios.update_one({'_id': ObjectId(id)}, {"$set": {
#         'producto': data['producto'],
#         'precio': precio,
#         'cantidad': cantidad,
#         'iva': iva,
#         'valor': valor_con_iva
#     }})
#     return jsonify({'message': 'Inventario Updated'})

@app.route('/inventarios/<id>', methods=['PUT'])
def updateInventario(id):
    data = request.json
    precio = float(data['precio'])
    cantidad = int(data['cantidad'])
    codigo= 'codigo',
    iva_rate = 0.12

    iva = precio * cantidad * iva_rate
    valor_con_iva = precio * cantidad * (1 + iva_rate)

    db_inventarios.update_one({'_id': ObjectId(id)}, {"$set": {
        'producto': data['producto'],
        'precio': precio,
        'cantidad': cantidad,
        'codigo' : codigo,
        'iva': iva,
        'valor': valor_con_iva
    }})
    return jsonify({'message': 'Inventario Updated'})



if __name__ == "__main__":
    app.run(debug=True)
