from flask import request, jsonify
import jwt
from dotenv import load_dotenv
import os
 
load_dotenv()
 
SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret")
 
token = None
 
def token_required(f):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
 
        if auth_header and auth_header.startswith("Bearer "):
            # getting the token
            token = auth_header.split(" ")[1]
 
        # if token is missing
        if not token:
            return jsonify({"error": "Token is missing"}), 401
 
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = decoded
        # If the token is expired or invalid
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
 
        return f(*args, **kwargs)
 
    # Preserve function metadata (e.g. name, docstring)
    wrapper.__name__ = f.__name__
    return wrapper