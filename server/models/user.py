from pydantic import BaseModel


class User(BaseModel):
    email: str
    name: str
    password: str
    authenticated: bool = False


class UserLogin(BaseModel):
    email: str
    password: str


class TokenData(BaseModel):
    username: str = None

