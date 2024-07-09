from pymongo import MongoClient
from pymongo.database import Database
print("hello from db")
client=MongoClient("mongodb+srv://dppatel:Admin1234@cluster0.ugxqzd8.mongodb.net/")
db=client.get_database("users_db")
try:
    client.admin.command('ping')
    print("Connected successfully")
except Exception as e:
    print(e)
def get_db() -> Database:
    return db
