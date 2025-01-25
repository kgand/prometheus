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

    return client["database"]


db = get_database()
