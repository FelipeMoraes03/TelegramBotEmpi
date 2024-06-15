from typing import Dict, List

class empiCollectionRepository:
    def __init__(self, db_connection) -> None:
        self.__collection_name = 'empiCollection'
        self.__db_connection = db_connection

    def insert_document(self, document: Dict) -> Dict:
        collection = self.__db_connection.get_collection(self.__collection_name)
        collection.insert_one(document)
        return document
    
    def insert_document_list(self, list: List[Dict]) -> List[Dict]:
        collection = self.__db_connection.get_collection(self.__collection_name)
        collection.insert_many(list)
        return list