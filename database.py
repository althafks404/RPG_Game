import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db      = client['mydatabase']

db_list = client.list_database_names()

if 'mydatabase' in db_list:
    print("db exist")
else:
    print("error")