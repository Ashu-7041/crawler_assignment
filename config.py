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
