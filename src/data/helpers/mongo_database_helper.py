from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import os

from ..interfaces import DatabaseHelper


class MongoDatabaseHelper(DatabaseHelper):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MongoDatabaseHelper, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):  # Prevent __init__ from running more than once
            self.__db_connection = self.connect('1mlet_embrapa')
            self._initialized = True

    def connect(self, db_name):
        load_dotenv()

        mongo_user = os.getenv('MONGO_INITDB_ROOT_USERNAME')
        mongo_pass = os.getenv('MONGO_INITDB_ROOT_PASSWORD')

        try:
            client = MongoClient(host='172.20.0.3', 
                                 port=27017,
                                 username=mongo_user,
                                 password=mongo_pass,
                                 authSource='admin')
            client.server_info() 
        except ServerSelectionTimeoutError as e:
            print(f"Error connecting to MongoDB: {e}")
            return None
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            return None

        db = client[db_name]
        return db

    def insert_many(self, collection, data):
        self.__db_connection[collection].insert_many(data)

    def find(self, collection, query):
        return self.__db_connection[collection].find(query)
