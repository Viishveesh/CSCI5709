from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_db
import re
from bson.json_util import dumps

app = Flask(__name__)
CORS(app)

# Initialize DB and Collection
db = get_db()
products_collection = db["products"]

#product's list
products = []

def validate(data):
    required_fields = ["name", "price", "description"]

    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    name_pattern = r"^[A-Za-z0-9\s\-']{2,100}$" 
    price_pattern = r"^\d+(\.\d{1,2})?$"
    description_pattern = r"^[A-Za-z\s]{2,50}$"

    if not re.fullmatch(name_pattern, str(data["name"])):
        print("not valid name")
        return False, "Product name must be 2–100 characters, letters/numbers only"

    if not re.fullmatch(price_pattern, str(data["price"])):
        print("not valid price")
        return False, "Price must be a number with up to 2 decimal places"

    if not re.fullmatch(description_pattern, str(data["description"])):
        print("not valid description")
        return False, "Description must be 2–50 characters, letters only"

    return True, None

@app.route("/products-info", methods=["GET"])
def fetch_products():
    products = list(products_collection.find({}, {"_id": 0}))
    return dumps(products), 200

# Add product
@app.route("/products-info", methods=["POST"])
def add_product():
    product_info = request.get_json()

    is_valid, error_msg = validate(product_info)

    print(is_valid)
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    products_collection.insert_one(product_info)
    return jsonify({"message": "Your Product has been added successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True)
