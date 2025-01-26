from pymongo import MongoClient
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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


def get_fastapi():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


db = get_database()
app = get_fastapi()
