""" 
MongoDB Interaction - A simple example for future developments
Fabio Bove | fabio.bove.dr@gmail.com
"""

#!/usr/bin/env python
# coding: utf-8

# Imports
import json
from pymongo import MongoClient

class MongoUtils:
    def __init__(self, auth_param: str, collection_name: str, database_name: str, data: json) -> None:
        self.mongo_client = None
        self.last_op_status = None
        self.auth_param = auth_param
        self.collection_name = collection_name
        self.database_name = database_name
        self.data = data
        self.database = None 

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

    
    def init_dabase(self):
        # Create (if don't exists yet) a new database on our cluster: "nasa"
        
        try: # Get the list of databases 
            db_list = self.mongo_client.list_database_names()
            self.last_op_status = "Got the list of active databases"
        except Exception as e:
            self.last_op_status = f"Can't get the list of database, {e}"
            return

        try:
            if self.database_name in db_list:
                self.last_op_status = f"Database {self.database_name} already exists."
                self.database = self.mongo_client.get_database(self.database_name)
            else:
                self.database = self.mongo_client[self.database_name]
                self.last_op_status = f"Database {self.database_name}  created successfully."
        except Exception as e:
            self.last_op_status = f"Something went wrong during database creation: \n {e}"
            self.database = None



    def init_cluster(self):
        self.connect_to_cluster()
        return True




     