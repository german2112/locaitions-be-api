import pymongo
import sys

try:
    client = pymongo.MongoClient("mongodb+srv://main:TiKeWoOMtmBml4Yo@locaitionscluster1.3vimx9r.mongodb.net/?retryWrites=true&w=majority")
except pymongo.errors.ConfigurationError:
  print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  sys.exit(1)

db = client.LOMNDB