from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
 
def get_db():
    try:
        client = MongoClient(os.environ.get("MONGO_URI"))
        db = client["productdb"]
        return db
    except ConnectionFailure:
        raise Exception("Could not connect to MongoDB. Is the server running?")