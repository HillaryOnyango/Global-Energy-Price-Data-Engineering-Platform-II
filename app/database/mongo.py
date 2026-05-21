from pymongo import MongoClient
from pymongo.database import Database

from app.config.settings import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class MongoDBClient:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_URI)
        self.db: Database = self.client[settings.MONGO_DB_NAME]

        logger.info("MongoDB connection initialized.")

    def get_database(self) -> Database:
        return self.db

    def close_connection(self):
        self.client.close()
        logger.info("MongoDB connection closed.")


mongodb = MongoDBClient()
db = mongodb.get_database()
