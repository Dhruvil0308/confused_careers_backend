from pymongo.database import Database
from auth import AuthHandler
from schemas import SignUp, Login
from fastapi import HTTPException

auth = AuthHandler()

def signup(db: Database, user: SignUp):
    hashed_password = auth.get_password_hash(user.password)
    admin_db = {
        "FirstName": user.FirstName,
        "LastName": user.LastName,
        "UserName": user.username,
        "hashed_password": hashed_password,
        "IsCreator": user.IsCreator,
        "MobileNumber": user.MobileNumber
    }
    result = db["Admin_data"].insert_one(admin_db)
    return {
        "FirstName": user.FirstName,
        "LastName": user.LastName,
        "UserName": user.username,
        "IsCreator": user.IsCreator,
        "MobileNumber": user.MobileNumber,
        "ID": str(result.inserted_id)
    }

def login(db: Database, user):
    admin_db = db["Admin_data"].find_one({"UserName": user.username})
    if not admin_db:
        return None
    if not auth.verify_password(user.password, admin_db["hashed_password"]):
        return None
    return admin_db
