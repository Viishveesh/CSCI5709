from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def get_db():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["productdb"]
        return db
    except ConnectionFailure:
        raise Exception("Could not connect to MongoDB. Is the server running?")
