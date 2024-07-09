from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
import os

# Load environment variables from .env file
load_dotenv(find_dotenv(filename=".env"))

class AuthHandler:
    security = OAuth2PasswordBearer(tokenUrl="token")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = os.getenv("SECRET_KEY")

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, username):
        payload = {
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow(),
            "sub": username
        }
        token = jwt.encode(payload, self.secret, algorithm="HS256")
        return token

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"]
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def auth_wrapper(self, auth: str = Depends(security)):
        return self.decode_token(auth)
