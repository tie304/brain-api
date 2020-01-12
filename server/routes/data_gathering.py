import json
from modules.auth import validate_current_user
from modules.auth import oauth2_scheme
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from workers.gather_google_images import gather_google_images

router = APIRouter()

@router.post("/gather-google-images/", status_code=201, tags=["data-gathering"])
async def collect(project: str, subclass: str, search_term: str, max_images: int, background_tasks: BackgroundTasks, token: str = Depends(oauth2_scheme)):
    username = await validate_current_user(token)
    background_tasks.add_task(gather_google_images, project=project, subclass=subclass, search_term=search_term, max_images=max_images, username=username)
    return "collection has been queued"
