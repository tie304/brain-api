import os
from fastapi import Depends, FastAPI
from pymodm import connect

import routes.users as users
import routes.data_gathering as data
import routes.trainer as trainer
import routes.classifcation_project as classifcation_project


from redis_conn import RedisConn

app = FastAPI()

connect(os.environ.get('MONGO_URI') + os.environ.get("MONGO_DB_NAME"))
RedisConn.initialize(os.environ.get('REDIS_HOST'), os.environ.get('REDIS_PORT'))

app.include_router(users.router)
app.include_router(data.router)
app.include_router(trainer.router)
app.include_router(classifcation_project.router)














