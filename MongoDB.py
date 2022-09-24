from pymongo import MongoClient

conn_str = 'mongodb://localhost:27017'
client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)
db = client.messagesApp









