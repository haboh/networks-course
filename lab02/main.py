from flask import Flask
from flask import request, abort
import json

app = Flask(__name__)

idCounter = -1
products = []

@app.route("/product", methods=["POST"])
def add_new_product():
    global products, idCounter

    data = json.loads(request.data)
    
    if 'name' not in data or 'description' not in data:
        abort(406)

    name, description = data['name'], data['description']
    idCounter += 1
    products.append({
        'id': idCounter,
        'name': name,
        'description': description,
    })

    return json.dumps({
        "id": idCounter,
        "name": name,
        "description": description
    })


def find_product_by_id(product_id):
    for product in products:
        if product['id'] == product_id:
            return product
    return None

@app.route("/product/<int:product_id>", methods=["GET", "DELETE", "PUT"])
def process_product(product_id):
    global products
    product = find_product_by_id(product_id)
    if product is None:
        abort(404)
    if request.method == "GET":
        return json.dumps(product)
    elif request.method == "DELETE":
        response = json.dumps(product)
        products.remove(product)
        return response
    elif request.method == "PUT":
        data = json.loads(request.data)
        if 'name' in data:
            product['name'] = data['name']
        if 'description' in data:
            product['description'] = data['description']
        return json.dumps(product)


@app.route("/products", methods=["GET"])
def get_products():
    global products

    return json.dumps(products)

if __name__ == '__main__':
    app.run()
