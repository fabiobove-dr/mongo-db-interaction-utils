       
"""
    def initialize_cluster():
        response = {'status': []}

        status, mongo_client = connect_to_cluster()
        response['status'].append(status)

        status, db = init_db(mongo_client)
        response['status'].append(status)

        status, collection = init_collection(db)
        response['status'].append(status)

        status, data = load_data_set()
        response['status'].append(status)

        status = init_documents(data, collection)
        response['status'].append(status)

        return response

    def init_collection(db):
        # Create a new collection in our db: "celestial_bodies"
        try:
            collections_list = db.list_collection_names()
            if COLLECTION in collections_list:
                status = "Collection already exists."
                collection = db.get_collection(COLLECTION)
            else:
                collection = db.celestial_bodies
                status = "Collection created successfully."
        except Exception as e:
            status = f"Something went wrong during collection creation: \n {e}"
            collection = None
        return status, collection


    def init_documents(data, collection):
        # Insert the document into our collection
        if collection.count_documents({}) > 0:  # We remove the old documents
            collection.delete_many({})
        try:
            [collection.insert_one(celestial_body) for celestial_body in data]
            status = "Documents loaded successfully."
        except Exception as e:
            status = f"Something went wrong during document insertion: \n {e}"
        return status
"""