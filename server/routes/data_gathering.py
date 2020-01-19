import json
from modules.auth import validate_current_user
from modules.auth import oauth2_scheme
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from redis_conn import RedisConn



router = APIRouter()

@router.post("/gather-google-images/", status_code=201, tags=["data-gathering"])
async def collect(project: str, subclass: str, search_term: str, max_images: int, token: str = Depends(oauth2_scheme)):
    username = await validate_current_user(token)
    data = {
        "project": project,
        "username": username,
        "subclass": subclass,
        "search_term": search_term,
        "max_images": max_images
    }
    data = json.dumps(data)
    RedisConn.CONN.rpush('gathering-queue', data)
    return "collection has been queued"
