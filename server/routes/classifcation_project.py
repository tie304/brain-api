import json
import datetime
from fastapi import APIRouter, HTTPException, Depends
from modules.auth import oauth2_scheme
from modules.auth import validate_current_user

from models.classification_project import CreateClassificationProject

from database.classification_project import ClassificationProject, ClassData
from database.user import User

router = APIRouter()


@router.post("/projects/classification_project", status_code=201, tags=["classification_project"])
async def create_classification_project(project: CreateClassificationProject, token: str = Depends(oauth2_scheme)):

    username = await validate_current_user(token)
    user = User.objects.get({"_id": username})
    created = datetime.datetime.now()
    # turn object into pymodm object
    classes = [ClassData(**vars(class_))for class_ in project.classes]
    #
    new_project = ClassificationProject(user=user, created=created, name=project.name,
                                    description=project.description,
                                    classes=classes)
    new_project.save()
    return "created project"



@router.get("/classification_project", status_code=200, tags=["classification_project"])
async def get_classification_project():
    pass


@router.delete("/classification_project", status_code=200, tags=["classification_project"])
async def delete_classification_project():
    pass


@router.put("/classification_project", status_code=200, tags=["classification_project"])
async def update_classification_project():
    pass
