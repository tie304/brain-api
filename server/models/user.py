from pydantic import BaseModel


class UserSignup(BaseModel):
    email: str
    name: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class TokenData(BaseModel):
    username: str = None

