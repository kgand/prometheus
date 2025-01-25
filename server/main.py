from bson.json_util import dumps as bson_dumps
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import OperationFailure
from dotenv import load_dotenv
from rich import print
from server.nps import get_filtered_webcams_list
import os


def get_database():
    load_dotenv()

    CONNECTION_STRING = os.environ.get("MONGODB_URI")

    client = MongoClient(CONNECTION_STRING)
    print("Connected to database")

    return client["database"]


# schema = {
#     "$jsonSchema": {
#         "bsonType": "object",
#         "properties": {
#             "lat": {"bsonType": "string"},
#             "long": {"bsonType": "string"},
#             "name": {"bsonType": "string"},
#             "image": {"bsonType": "string"},
#         },
#     }
# }


db = get_database()
parkcams = db.parkcams


def populate_database(webcams: list):
    for webcam in webcams:
        parkcams.insert_one(webcam)


# NOTE: this be it
# populate_database(get_filtered_webcams_list())
# print(
#     bson_dumps(
#         parkcams.find_one({"id": "C734932D-DB0B-467A-82DB-6D6A3873BC6A"}), indent=4
#     )
# )
