""" 
MongoDB Interaction - A simple example for future developments
Fabio Bove | fabio.bove.dr@gmail.com
"""

#!/usr/bin/env python
# coding: utf-8

# Imports
from pymongo import MongoClient

class MongoUtils:
    def __init__(self, auth_param: str, collection_name: str, database_name: str, data: dict) -> None:
        self.mongo_client       = None
        self.last_op_status     = None
        self.database           = None 
        self.collection         = None 
        self.auth_param         = auth_param
        self.collection_name    = collection_name
        self.database_name      = database_name
        self.data               = data

    def get_last_op_status(self) -> str:
        """
        get_last_op_status, this method returns a string containing the status of the last operation made by this class

        param: None
        return: last_op_status: A string containing the status of the last operation made by this class
        """
        return self.last_op_status

    def connect_to_cluster(self) -> None:
        """ 
            connect_to_cluster, this method allow to instantiate a new cluster Connection 

            pram: None
            return: None
        """
        try:
            self.mongo_client = MongoClient(self.auth_param)
            self.last_op_status = "Successfully connected to cluster."
        except Exception as e:
            self.last_op_status = f"Something went wrong during cluster connection: \n {e}"
            self.mongo_client = None

        
    def init_dabase(self, database_name:str):
        """
            create_dabase method, creates (if don't exists yet) a new database with name <database_name>

            param: database_name: A string with the name of the new database
            return: Nothing
        """
        try: # Get the list of databases 
            db_list = self.mongo_client.list_database_names()
            self.last_op_status = "Got the list of active databases"
        except Exception as e:
            self.last_op_status = f"Can't get the list of database, {e}"
            return
        try:
            if database_name in db_list:
                self.last_op_status = f"Database {database_name} already exists."
                self.database = self.mongo_client.get_database(database_name)
            else:
                self.database = self.mongo_client[database_name]
                self.last_op_status = f"Database {database_name}  created successfully."
        except Exception as e:
            self.last_op_status = f"Something went wrong during database creation: \n {e}"
            self.database = None  

    def init_collection(self, collection_name:str):
        # Create a new collection in our db: "celestial_bodies"
        try:
            collections_list = self.database.list_collection_names()
            if collection_name in collections_list:
                self.last_op_status = f"Collection already exists."
                self.collection = self.database.get_collection(collection_name)
            else:
                self.collection = self.database[collection_name]
                self.last_op_status = f"Collection {collection_name} created successfully."
        except Exception as e:
            self.last_op_status = f"Something went wrong during collection creation: \n {e}"
            self.collection = None
       

    def init_documents(self, data):
        """
        init_documents method, inserts the documents into our collection
        """
        if self.collection.count_documents({}) > 0:  # We remove the old documents
            self.collection.delete_many({})
        try:
            [self.collection.insert_one(elem) for elem in data]
            self.last_op_status = f"Documents loaded successfully."
        except Exception as e:
           self.last_op_status = f"Something went wrong during document insertion: \n {e}"
        



     
    def init_cluster(self):
        self.connect_to_cluster()
        self.init_dabase(self.database_name)
        self.init_collection(self.collection_name)
        self.init_documents(self.data)