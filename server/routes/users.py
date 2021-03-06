import jwt
import pymodm.errors as DBerrors
from fastapi import APIRouter, HTTPException, Depends
from models.user import UserSignup, UserLogin
from modules.auth import *
from database.user import User

router = APIRouter()


@router.post("/sign-up", status_code=201, tags=["users"])
async def create_user(user_signup: UserSignup):
    print("SIGNING UP")
    email = user_signup.email
    try:
        usr = User.objects.get({'_id': email})
        if usr:
            raise HTTPException(status_code=400, detail="email already in use")
    except DBerrors.DoesNotExist:
        # hash password
        user_signup.password = pwd_context.hash(user_signup.password)
        # save new user
        User(email=user_signup.email, name=user_signup.name, password=user_signup.password).save()
    return "user created"


@router.post("/login", tags=["users"])
async def login_user(user_login: UserLogin):
    email, password = user_login.email, user_login.password
    try:
        find_user = User.objects.get({'_id': email})
    except DBerrors.DoesNotExist:
        raise HTTPException(status_code=404, detail="User Does Not Exist")

    if not find_user:
        return HTTPException(status_code=404, detail="user not found")
    if verify_password(password, find_user.password):
        access_token = create_access_token(
            data={"sub": email})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code = 401, detail="Invalid password")











