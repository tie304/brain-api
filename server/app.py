from fastapi import Depends, FastAPI


import routes.users as users
import routes.data_gathering as data
import routes.trainer as trainer
from database import Database
from redis_conn import RedisConn


app = FastAPI()
Database.initialize("mongodb://mongo:27017/","image-detector")
RedisConn.initialize('redis',6379)

app.include_router(users.router)
app.include_router(data.router)
app.include_router(trainer.router)














