from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def get_mongo():
    client = MongoClient(URL, server_api=ServerApi('1'))
    try:
        # Access the database and collection
        db = client['Tweet_tg']
        collection = db['my_first_data']
  
        # Retrieve a single document from the collection based on the query
        document = collection.find_one()
  
        try:
            return document
        except Exception as e:
            print(f"Error writing JSON data: {e}")
  
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None
  
    finally:
        # Close the connection in a finally block to ensure it is always closed
        client.close()




def mongo_update(files, remove=False, set_empty=False):
    """
    files: dict, Json ; defines the json or dictionary to be updated
    remove: str ; defines the keys to be removed. If you want to remove a key inside a key, separate the keys with a dot.
    set_empty: bool ; will remove all data in the collection
    """
    try:
        client = MongoClient(URL, server_api=ServerApi('1'))
        db = client['Tweet_tg']
        collection = db['my_first_data']
        document = collection.find_one()

        # Exclude '_id' field from the update query
        files_without_id = files.copy()
        files_without_id.pop('_id', None)

        if remove:
            keys = remove.split('.')
            nested_dict = data
            for key in keys[:-1]:
                nested_dict = nested_dict[key]
            del nested_dict[keys[-1]]
        if set_empty:
            for key in files_without_id:
                collection.update_one({"_id": document["_id"]}, {"$unset": {key: ""}})
        else:
            update_query = {"$set": files_without_id}
            collection.update_one({"_id": document["_id"]}, update_query)

        # Return the modified files dictionary
        return files_without_id
    except Exception as e:
        print(f"Error updating document: {e}")
    finally:
        client.close()
