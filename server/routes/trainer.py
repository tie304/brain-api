import json
from fastapi import APIRouter, HTTPException, Depends
from redis_conn import RedisConn
from modules.auth import oauth2_scheme
from modules.auth import validate_current_user


router = APIRouter()


@router.post("/train/", status_code=201, tags=["trainer"])
async def collect(project: str, batch_size: int, epochs: int, test_size: int, token: str = Depends(oauth2_scheme)):
    username = await validate_current_user(token)
    data = {
        "project": project,
        "username": username,
        "batch_size": batch_size,
        "epochs": epochs,
        "test_size": test_size
    }
    data = json.dumps(data)
    RedisConn.CONN.rpush('training-queue', data)

    return "your training job as queued"