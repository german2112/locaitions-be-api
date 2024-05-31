import pymongo
import sys

try:
    client = pymongo.MongoClient("mongodb+srv://loglobalproject:v0yzLDCHXgpDkGwp@locaitionscluster1.c7gk29f.mongodb.net/?retryWrites=true&w=majority&appName=locaitionscluster1") #TODO Find a way to hide the password from the uri
except pymongo.errors.ConfigurationError:
  print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  sys.exit(1)

db = client.LOMNDB