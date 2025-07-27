from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import jwt
from pymongo import MongoClient
from bson import ObjectId
import bcrypt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
from flask_cors import CORS
from prometheus_client import generate_latest
from prometheus_flask_exporter import PrometheusMetrics

load_dotenv()
app = Flask(__name__)
metrics = PrometheusMetrics(app, path='/metrics')
# cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('SENDER_EMAIL')
app.config['MAIL_PASSWORD'] = os.getenv('SENDER_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('SENDER_EMAIL')

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.mediconnect
users_collection = db.users

# Create index on email field
users_collection.create_index("email", unique=True)

@app.route('/metrics')
def metrics_endpoint():
    return generate_latest(), 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}

@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    if users_collection.find_one({"email": email}):
        return jsonify({"message": "User already exists!"}), 400
    # Use bcrypt with reduced work factor (10)
    hashed_password = bcrypt.hashpw(data.get("password").encode('utf-8'), bcrypt.gensalt(rounds=10))
    user = {
        "firstName": data.get("firstName"),
        "lastName": data.get("lastName"),
        "email": email,
        "password": hashed_password,
        "role": data.get("role")
    }
    users_collection.insert_one(user)
    return jsonify({"message": "Signup successful!"}), 201

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    user = users_collection.find_one({"email": email})
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return jsonify({"message": "Invalid Credentials"}), 401
    token = jwt.encode({
        "email": email,
        "role": user.get("role"),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({
        "token": token,
        "role": user.get("role"),
        "name": f"{user.get('firstName', '')} {user.get('lastName', '')}".strip(),
        "email": user.get("email")
    })

@app.route("/api/request-reset", methods=["POST"])
def request_password_reset():
    data = request.json
    email = data.get("email")
    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"message": "No account with that email."}), 404
    token = serializer.dumps(email, salt="password-reset-salt")
    reset_link = f"http://localhost:3000/reset-password?token={token}"
    try:
        msg = Message("Password Reset Request", recipients=[email])
        msg.body = f"Hi {user.get('firstName', '')},\n\nTo reset your password, click the following link:\n\n{reset_link}\n\nIf you did not request this, please ignore this email.\n\nThanks!"
        mail.send(msg)
    except Exception as e:
        print(f"Email sending failed: {e}")
        return jsonify({"message": "Failed to send reset email."}), 500
    return jsonify({"message": "Password reset link sent to your email."})

@app.route("/api/reset-password", methods=["POST"])
def reset_password():
    data = request.json
    token = data.get("token")
    new_password = data.get("newPassword")
    try:
        email = serializer.loads(token, salt="password-reset-salt", max_age=3600)
    except Exception as e:
        return jsonify({"message": "Invalid or expired token."}), 400
    # Use bcrypt with reduced work factor (10)
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt(rounds=10))
    result = users_collection.update_one(
        {"email": email},
        {"$set": {"password": hashed_password}}
    )
    if result.modified_count == 1:
        return jsonify({"message": "Password updated successfully."})
    else:
        return jsonify({"message": "Something went wrong."}), 500

# @app.after_request
# def apply_security_headers(response):
#     response.headers['Permissions-Policy'] = 'geolocation=(), camera=(), microphone=(), payment=(), usb=()'
#     response.headers['X-Frame-Options'] = 'DENY'
#     return response

if __name__ == "__main__":
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule} -> {rule.endpoint}")
    app.run(debug=True, host="0.0.0.0", port=5000)