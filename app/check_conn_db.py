import pymongo
from dotenv import dotenv_values
import os
if os.path.exists('.env'):
    configs = dotenv_values(".env")
else:
    configs = os.environ
client = pymongo.MongoClient(configs['MONGO_URL'])

info = client.server_info()
# pprint(info)

# db = client["test_db"]
# collection = db["test_collection"]

# # create a new database
# db = client["mydatabase"]

# # create a new collection
# collection = db["mycollection"]

# # show all database
# pprint(client.list_database_names())

# # show all collection
# pprint(db.list_collection_names())

# # insert a new document
# post = {"author": "Mike", "text": "My first blog post!", "tags": ["mongodb", "python", "pymongo"]}
# collection.insert_one(post)

# # find all documents
# for post in collection.find():
#     pprint(post)