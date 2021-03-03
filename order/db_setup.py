from pymongo import MongoClient
from pymongo.errors import CollectionInvalid,ConnectionFailure,DuplicateKeyError,OperationFailure,PyMongoError

#connection class
class MongoConnection():

    def __init__(self):
        try:
            self.client = MongoClient('localhost', 27017)
            self.db = self.client['OrderBills']
            print("Connection successful! xD")
        except ConnectionFailure:
            print("DB Connection failed!")


    def get_collection(self, name):
        print("Trying to retrieve collection!")
        try:
            self.collection = self.db[name]
            return self.collection
        except CollectionInvalid:
            print("Invalid collection :P")

#retrieve - collection
class MyCollection(MongoConnection):

    def __init__(self):
       super(MyCollection, self).__init__()
       #self.get_collection(collection_name)

    def get_collection(self, name):
        return super().get_collection(name)

def insert_one_doc(collection,doc):
        try:
            collection.insert_one(doc)
        except DuplicateKeyError:
            print("Duplicate Key _id - inserted")
        except OperationFailure:
            print("Insert operation failed")
        except PyMongoError:
            print("Insert - Unknown error")

def find_doc(collection,key=None,value=None):
        try:
            if key==None:
                return list(collection.find({}))
            else:
                return collection.find_one({key:value})
        except OperationFailure:
            print("Unable to find document!")
        except PyMongoError:
            print("Find - unknown error")


def update_doc(collection,key,value):
        myquery = {key:value}
        newvalues = {"$set": {"availability": False}}
        try:
            collection.update_one(myquery, newvalues)
        except OperationFailure:
            print("Unable to Update document!")
        except PyMongoError:
            print("Update - unknown error")
