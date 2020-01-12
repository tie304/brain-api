import jwt
from fastapi import APIRouter, HTTPException, Depends

from modules.auth import *
from models.user import User, UserLogin
from database import Database
from datetime import datetime, timedelta


router = APIRouter()



@router.post("/sign-up/", status_code=201, tags=["users"])
async def create_user(user: User):
    email = user.email
    if Database.find_one('users', {"email": email}):
        return HTTPException(status_code=400, detail="email already in use")
    # hash password
    user.password = pwd_context.hash(user.password)
    # save new user
    Database.insert('users', user.dict())
    return "user created"


@router.post("/login", tags=["users"])
async def login_user(user: UserLogin):
    email, password = user.email, user.password
    find_user = Database.find_one('users', {"email": email})
    if not find_user:
        return HTTPException(status_code = 404, detail="user not found")
    if verify_password(password, find_user['password']):
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": email}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    return HTTPException(status_code = 401, detail="Invalid password")











