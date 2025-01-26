from connect import db


def get_camera_by_camera_id(id):
    images = db.fire_detections

    # do not include _id (ObjectId)
    return images.find_one({"camera_id": id}, {"_id": False})
