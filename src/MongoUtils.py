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
        self.database_list      = None
        self.collections_list   = None
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
            connect_to_cluster, this method allow to instantiate a new cluster Connection using the pymongo lib
            
            pram: None
            return: None
        """
        try:
            self.mongo_client = MongoClient(self.auth_param)
            self.last_op_status = "Successfully connected to Mongo Cluster"
        except Exception as e:
            self.last_op_status = f"Something went wrong during cluster connection: \n {e}"
            self.mongo_client = None

    def init_dabase(self, database_name:str) -> None:
        """
            init_dabase method, creates (if don't exists yet) a new database with name <database_name>

            param: database_name: A string with the name of the new database
            return: Nothing
        """
        try: # Get the list of databases for the current cluster
            self.database_list = self.mongo_client.list_database_names()
            self.last_op_status = f"Got the list of active databases: \n {self.database_list}"
        except Exception as e:
            self.last_op_status = f"Can't get the list of databases: \n {e}"
            self.database_list = None

        try:
            if self.database_list is not None and database_name in self.database_list:
                self.last_op_status = f"Database {database_name} already exists."
                self.database = self.mongo_client.get_database(database_name)
            else:
                self.database = self.mongo_client[database_name]
                self.last_op_status = f"Database <{database_name}> created successfully."
        except Exception as e:
            self.last_op_status = f"Something went wrong during database creation: \n {e}"
            self.database = None  

    def init_collection(self, collection_name:str):
        """
        init_collection method, initialize a collection if doesn't exists already otherwhise returns the existing one

        param: collection_name: The name of the collection 
        return: Nothing
        """
        try:
            self.collections_list = self.database.list_collection_names()
        except Exception as e:
            self.last_op_status = f"Can't get the list of collection: \n {e}"
            self.collection = None
            self.collections_list = None
        try:
            if self.collections_list is not None and collection_name in  self.collections_list:
                self.last_op_status = f"Collection already exists."
                self.collection = self.database.get_collection(collection_name)
            else:
                self.collection = self.database[collection_name]
                self.last_op_status = f"Collection <{collection_name}> created successfully."
        except Exception as e:
            self.last_op_status = f"Something went wrong during collection creation: \n {e}"
            self.collection = None
       
    def init_documents(self, data:dict) -> None:
        """
        init_documents method, inserts the documents into our collection taken from the given data

        param: data: a dict containing all the data to load in the collection
        return: Nothing
        """
        try:
            self.collection.insert_many(data) # [self.collection.insert_one(elem) for elem in data]
            self.last_op_status = f"Documents loaded successfully."
        except Exception as e:
           self.last_op_status = f"Something went wrong during document insertion: \n {e}"
    
    def clean_collection(self, collection_name: str) -> None:
        """
        clean_collection method, remove all the documents of a collection

        param: collection_name: A string containing the name of the collection.
        return: Nothing
        """
        if collection_name is not None: # Load the desired collection, if collection_name is empty use the last collection connected to the class
            self.init_collection(collection_name)
        if self.collection is not None:
            if self.collection.count_documents({}) > 0:  # Remove the old documents
                self.collection.delete_many({})
                self.last_op_status = f"Removed old files from the collection."

    def init_cluster(self):
        self.connect_to_cluster()
        self.init_dabase(self.database_name)
        self.init_collection(self.collection_name)
        self.init_documents(self.data)