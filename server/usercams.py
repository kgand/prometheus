from connect import db, app


def add_new_usercam(
    name,
    ip_address,
    user_id,
    latitude,
    longitude,
):
    usercams = db.user_cctv

    if not all([name, ip_address, user_id, latitude, longitude]):
        raise ValueError("One or more values are None or falsy, nothing added")

    usercams.insert_one(
        {
            "name": name,
            "ip_address": ip_address,
            "user_id": user_id,
            "latitude": latitude,
            "longitude": longitude,
        }
    )
