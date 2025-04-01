import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from typing import Dict, List

import structlog
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

from config import MONGODB_URI
from logger import configure_logging

configure_logging()
logger = structlog.get_logger(__name__)

class MongoDB:
    class MongoDBError(Exception):
        pass

    def __init__(self, db_name: str):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[db_name]
        
    def save_documents(self, collection_name: str, documents: List[Dict]):
        try:
            conn = self.db[collection_name]
            conn.insert_many(documents)
        except BulkWriteError as e:
            logger.error(f"Error saving documents to MongoDB: {e}")
            raise self.MongoDBError(f"Error saving documents to MongoDB: {e}")
        
    def fetch_documents(self, collection_name: str, query: dict):
        try:
            conn = self.db[collection_name]
            return conn.find_one(query)
        except Exception as e:
            logger.error(f"Error fetching documents from MongoDB: {e}")
            raise self.MongoDBError(f"Error fetching documents from MongoDB: {e}")
        
    def fetch_all_documents(self, collection_name: str, query: dict):
        try:
            conn = self.db[collection_name]
            return conn.find(query)
        except Exception as e:
            logger.error(f"Error fetching documents from MongoDB: {e}")
            raise self.MongoDBError(f"Error fetching documents from MongoDB: {e}")

