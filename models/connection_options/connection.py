from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values

config = dotenv_values(".env")

class dbConnectionHaddler:
    def __init__(self) -> None:
        self.__uri = "mongodb+srv://{}:{}@{}/?retryWrites=true&w=majority&appName={}".format(
            config['MONGO_USERNAME'],
            config['MONGO_PASSWORD'],
            config['MONGO_HOST'],
            config['MONGO_DB_CLUSTER']
        )
        self.__db_name = config['MONGO_DB_NAME']
        self.__client = None
        self.__db_connection = None


    # METHODS
    def connect_db(self):
        self.__client = MongoClient(self.__uri)
        self.__db_connection = self.__client[self.__db_name]

    # GETTERS
    def get_db_client(self):
        return self.__client

    def get_db_connection(self):
        return self.__db_connection