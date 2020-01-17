import json
import datetime
from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException, Depends
from modules.auth import oauth2_scheme
from modules.auth import validate_current_user

from models.classification_project import CreateClassificationProject, GetClassificationProject, GetClassificationProjects
from database.classification_project import ClassificationProject, ClassData
from database.user import User
from modules.pymodm_bridge import PymodmPydanticBridge

router = APIRouter()


@router.post("/projects/classification_project", status_code=201, tags=["classification_project"])
async def create_classification_project(project: CreateClassificationProject, token: str = Depends(oauth2_scheme)):

    username = await validate_current_user(token)
    user = User.objects.get({"_id": username})
    projects = ClassificationProject.objects.raw({'user': username})

    # check if user has already created a project
    for p in projects:
        if p.name == project.name:
            return HTTPException(status_code=400, detail="Project name already created. Please chose another or delete existing one.")

    created = datetime.datetime.now()
    # turn object into pymodm object from
    classes = PymodmPydanticBridge.pydatic_to_pymodm(project.classes, target_class="ClassData")

    new_project = ClassificationProject(user=user, created=created, name=project.name,
                                    description=project.description,
                                    classes=classes)
    new_project.save()
    return "created project"


@router.get("/projects/classification_project", status_code=200, response_model=GetClassificationProject, tags=["classification_project"])
async def get_classification_project_by_id(_id: str, token: str = Depends(oauth2_scheme)):
    await validate_current_user(token)
    db_project = ClassificationProject.objects.get({'_id': _id})
    project = PymodmPydanticBridge.pymodm_to_pydantic(db_project, target_class="GetClassificationProject")
    return project


@router.get("/projects/classification_project/all", status_code=200, response_model=GetClassificationProjects, tags=["classification_project"])
async def get_classification_project_by_id(token: str = Depends(oauth2_scheme)):
    username = await validate_current_user(token)
    db_projects = ClassificationProject.objects.raw({'user': username})
    # returns a list of single projects
    # response_model expects {'projects': projects}
    projects = PymodmPydanticBridge.pymodm_to_pydantic(db_projects, target_class="GetClassificationProject")
    return {'projects': projects}


@router.delete("/classification_project", status_code=200, tags=["classification_project"])
async def delete_classification_project():
    pass


@router.put("/classification_project", status_code=200, tags=["classification_project"])
async def update_classification_project():
    pass
