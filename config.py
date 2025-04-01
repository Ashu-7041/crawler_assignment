import os
from dotenv import load_dotenv

load_dotenv()

BROKER_URL="redis://localhost:6379/4"
MONGODB_USER = os.getenv("MONGODB_USER")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_HOST = os.getenv("MONGODB_HOST")
MONGODB_PORT = os.getenv("MONGODB_PORT")
MONGODB_AUTH_DB = os.getenv("MONGODB_AUTH_DB")

MONGODB_URI = f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/?authSource={MONGODB_AUTH_DB}"
MONGODB_URI = "mongodb://ashutosh:05ca0c579751eafeaeea475c1a26d4463e837a5a@101.53.134.233:39717/admin"