from flask import Flask, jsonify, request
from store import stores

app = Flask(__name__)


# STORE FUNCTIONALITY OR RESOURCE
@app.route("/stores", methods=['GET'])
def get_stores():
    return jsonify(stores)


@app.route("/stores/<string:name>", methods=['GET'])
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'}), 200


@app.route("/stores", methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    for store in stores:
        if store['name'] == new_store['name']:
            return jsonify({"message": "store already exists"}), 409
    stores.append(new_store)
    return jsonify(stores)


@app.route("/stores/<string:name>", methods=['DELETE'])
def delete_store(name):
    for store in stores:
        if store['name'] == name:
            stores.remove(store)
            return jsonify(stores), 200
    return jsonify({"message": "store does not exists"})


@app.route("/stores/<string:name>", methods=['PUT'])
def update_store(name):
    store_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            stores.remove(store)
            stores.append(store_data)
            return jsonify({"message": f"{name} updated successfully"}), 200
    return jsonify({"message": "store does not exists"}), 404


# ITEMS FUNCTIONALITY
@app.route("/stores/<string:name>/items", methods=['GET'])
def get_items_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store['items']), 200
    return jsonify({'message': "Store Not Found"}), 404


@app.route("/stores/<string:name>/items/<string:itemName>", methods=['GET'])
def get_item_store(name, itemName):
    for store in stores:
        if store['name'] == name:
            for item in store['items']:
                if item['name'] == itemName:
                    return jsonify(item), 200
    return jsonify({'message': "Item Not Found"}), 404


@app.route("/stores/<string:name>/items/<string:itemName>", methods=['PUT'])
def update_item_store(name, itemName):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            for item in store['items']:
                if item['name'] == itemName:
                    new_item = {'name': request_data['name'], 'price': request_data['price']}
                    store['items'].remove(item)
                    store['items'].append(new_item)
                    return jsonify(new_item), 200
    return jsonify({'message': "Item Not Found"}), 404


@app.route("/stores/<string:name>/items/<string:itemName>", methods=['POST'])
def add_item_store(name, itemName):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            found = any(itemName in d.values() for d in store['items'])
            if found:
                return jsonify({'message': "Item already exists"}), 409
            else:
                new_item = {'name': itemName, 'price': request_data['price']}
                store['items'].append(new_item)
                return jsonify(store), 201


@app.route("/stores/<string:name>/items/<string:itemName>", methods=['DELETE'])
def delete_item_store(name, itemName):
    for store in stores:
        if store['name'] == name:
            for item in store['items']:
                if item['name'] == itemName:
                    store['items'].remove(item)
                    return jsonify({'message': f"{itemName} successfully deleted"}), 204
    return jsonify({'message': "Item Not Found"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5001)
