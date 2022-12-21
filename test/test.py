import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)

from src.MongoUtils import MongoUtils
import yaml
import json

# Configuration Parameters for MongoDB connection

# Load the oauth_settings.yml file
stream          = open('oauth_settings.yml', 'r')
settings        = yaml.load(stream, yaml.SafeLoader)
dataset_path    = settings['dataset_path']
auth_param      = settings['auth_param']
collection_name = settings['collection_name']
database_name   = settings['database_name'] 

def import_data(data_path: str) -> json or None:
    try:
        f = open(data_path) # Opening JSON file
        data = json.load(f)
        return data
    except Exception as e:
        print(f"Can't read data from path: {data_path}, {e}")
    return None

def main():
    data = import_data(data_path=dataset_path)
    mongo_utils = MongoUtils(
        auth_param=auth_param, 
        collection_name=collection_name, 
        database_name=database_name, 
        data=data
    )

    mongo_utils.connect_to_cluster()
    print(mongo_utils.get_last_op_status())
    """
    mongo_utils.init_dabase(database_name=database_name)
    print(mongo_utils.get_last_op_status())

    mongo_utils.init_collection(collection_name=collection_name)
    print(mongo_utils.get_last_op_status())

    mongo_utils.init_documents(data=data)
    print(mongo_utils.get_last_op_status())
    """

if __name__ == "__main__":
    main()