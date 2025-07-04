from flask import Flask, request, jsonify
import bcrypt
import jwt
from flask_cors import CORS
from db import get_db
import re
from bson.json_util import dumps
import datetime
from auth_middleware import token_required
from dotenv import load_dotenv
import os
 
load_dotenv()
 
app = Flask(__name__)
CORS(app)
SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret")
 
 
# Initialize DB and Collection
db = get_db()
products_collection = db["products"]
 
users_collection = db["users"]
 
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
@token_required
def fetch_products():
    products = list(products_collection.find({}, {"_id": 0}))
    return dumps(products), 200
 
# Add product
@app.route("/products-info", methods=["POST"])
@token_required
def add_product():
    product_info = request.get_json()
 
    is_valid, error_msg = validate(product_info)
 
    print(is_valid)
    if not is_valid:
        return jsonify({"error": error_msg}), 400
 
    products_collection.insert_one(product_info)
    return jsonify({"message": "Your Product has been added successfully"}), 201
 
# Register route
@app.route("/api/auth/register", methods=["POST"])
def register_user():
    data = request.get_json()
 
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
 
    # if any field is missing
    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400
 
    # check if user already exists
    if users_collection.find_one({"email": email}):
        return jsonify({"error": "Email already registered"}), 409
 
    # hash the password
    hash_pwd = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
 
    # store user
    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": hash_pwd
    })
 
    # generate JWT Token
    token = jwt.encode({
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, SECRET_KEY, algorithm="HS256")
 
    return jsonify({"message": "User registered successfully", "token": token}), 201
 
 
# Login route
@app.route("/api/auth/login", methods=["POST"])
def login_user():
    data = request.get_json()
 
    email = data.get("email")
    password = data.get("password")
 
    # if any field is missing
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
 
    # if user is not available
    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401
 
    # if password is not matching
    if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return jsonify({"error": "Invalid email or password"}), 401
 
    # generate JWT Token
    token = jwt.encode({
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, SECRET_KEY, algorithm="HS256")
 
    return jsonify({"message": "Login successful", "token": token}), 200
 
 
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)