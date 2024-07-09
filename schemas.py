from pydantic import BaseModel

class SignUp(BaseModel):
    FirstName: str
    LastName: str
    username: str
    password: str
    IsCreator: bool
    MobileNumber: str

class Login(BaseModel):
    username: str
    password: str
