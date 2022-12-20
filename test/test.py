from src.MongoUtils import MongoUtils
import os
import json

# Configuration Parameters for MongoDB connection
AUTH_PARAM = "" # auth string
DATABASE = "nasa" # database name
COLLECTION = "celestial_bodies" # collection name
DATA_SET_PATH = "dataset/dataset.json" # dataset path (dataset should be a .json file)

def import_data(data_path: str) -> json or None:
    try:
        f = open(data_path) # Opening JSON file
        data = json.load(f)
        return data
    except Exception as e:
        print(f"Can't read data from path: {data_path}, {e}")
    return None

def main():
    data = import_data(data_path=DATA_SET_PATH)
    mongo_utils = MongoUtils(
        auth_param=AUTH_PARAM, 
        collection_name=COLLECTION, 
        database_name=DATABASE, 
        data=data
    )
    mongo_utils.connect_to_cluster()
    print(mongo_utils.get_last_op_status())

    mongo_utils.init_dabase(database_name=DATABASE)
    print(mongo_utils.get_last_op_status())

    mongo_utils.init_collection(collection_name=COLLECTION)
    print(mongo_utils.get_last_op_status())

    mongo_utils.init_documents(data=data)
    print(mongo_utils.get_last_op_status())


if __name__ == "__main__":
    main()