from connect import db
from rich import print
# from nps import get_filtered_webcams_list

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
