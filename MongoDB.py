from pymongo import MongoClient

conn_str = 'mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=rs0'
client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)
db = client.messagesApp









