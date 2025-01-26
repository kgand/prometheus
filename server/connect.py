from pymongo import MongoClient
from dotenv import load_dotenv
from rich import print
import os


def get_database():
    load_dotenv()

    CONNECTION_STRING = os.environ.get("MONGODB_URI")

    print(CONNECTION_STRING)

    client = MongoClient(CONNECTION_STRING)
    print("Connected to database")

    db = client.database

    # Collections
    parkcams = db.parkcams
    user_cctv = db.user_cctv
    fire_detections = db.fire_detections

    return db


db = get_database()
