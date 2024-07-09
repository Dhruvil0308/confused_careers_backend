from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import get_db
from pymongo.database import Database
from auth import AuthHandler
from models import signup, login
from schemas import Login, SignUp

app = FastAPI()
auth = AuthHandler()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/register")
async def Register(user: SignUp, db: Database = Depends(get_db)):
    db_user = db["Admin_data"].find_one({"UserName": user.username})
    if db_user:
        raise HTTPException(status_code=400, detail="User Already Exists")
    return signup(db, user)

@app.post("/token", tags=["authentication"])
async def Access_Login(form_data: OAuth2PasswordRequestForm = Depends(), db: Database = Depends(get_db)):
    user_login = Login(username=form_data.username, password=form_data.password)
    authenticated_user = login(db, user_login)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = auth.encode_token(authenticated_user["UserName"])
    return {"access_token": token, "token_type": "bearer"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
