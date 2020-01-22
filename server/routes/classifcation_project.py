import json
import datetime
import pymodm.errors as DBerrors
from fastapi import APIRouter, HTTPException, Depends
from modules.auth import oauth2_scheme
from modules.auth import validate_current_user

from redis_conn import RedisConn
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

    # turn object into pymodm object from
    classes = PymodmPydanticBridge.pydatic_to_pymodm(project.classes, target_class="ClassData")
    new_project = ClassificationProject(user=user, name=project.name, description=project.description,
                                        classes=classes)
    new_project.save()
    return "created project"


@router.get("/projects/classification_project", status_code=200, response_model=GetClassificationProjects, tags=["classification_project"])
async def get_classification_project_by_id(_id: str, token: str = Depends(oauth2_scheme)):
    await validate_current_user(token)
    try:
        db_project = ClassificationProject.objects.get({'_id': _id})
    except DBerrors.DoesNotExist:
        return HTTPException(detail="Project doesn't exist", status_code=400)

    project = PymodmPydanticBridge.pymodm_to_pydantic(db_project, target_class="GetClassificationProject")
    return {'projects': [project]}


@router.delete("/projects/classification_project", status_code=200, tags=["classification_project"])
async def delete_classification_project(_id: str, token: str = Depends(oauth2_scheme)):
    username = await validate_current_user(token)
    try:
        ClassificationProject.objects.get({'_id': _id}).delete()
    except DBerrors.DoesNotExist:
        return HTTPException(detail="Project doesn't exist", status_code=400)
    return "project deleted"


@router.get("/projects/classification_project/all", status_code=200, response_model=GetClassificationProjects, tags=["classification_project"])
async def get_classification_project_by_id(token: str = Depends(oauth2_scheme)):
    username = await validate_current_user(token)
    db_projects = ClassificationProject.objects.raw({'user': username})

    # returns a list of single projects
    # response_model expects {'projects': projects}
    projects = PymodmPydanticBridge.pymodm_to_pydantic(db_projects, target_class="GetClassificationProject")

    if not isinstance(projects, list):
        return {'projects': [projects]}
    return {'projects': projects}



@router.put("/projects/classification_project", status_code=200, tags=["classification_project"])
async def update_classification_project(_id: str, project_update: CreateClassificationProject, token: str = Depends(oauth2_scheme)):
    user = await validate_current_user(token)
    try:
        ClassificationProject.objects.get({'_id': _id})
    except DBerrors.DoesNotExist:
        return HTTPException(detail="Project doesn't exist!", status_code=404)

    classes = PymodmPydanticBridge.pydatic_to_pymodm(project_update.classes, target_class="ClassData")
    project = PymodmPydanticBridge.pydatic_to_pymodm(project_update, target_class="ClassificationProject")

    project.classes = classes
    project._id = _id
    project.user = user

    project.save()
    return "project updated"


@router.post("/projects/classification_project/collect_google_images", status_code=200, tags=["classification_project"])
async def collect_project_images(_id: str, token: str = Depends(oauth2_scheme)):
    user = await validate_current_user(token)
    try:
        project = ClassificationProject.objects.get({'_id': _id})
    except DBerrors.DoesNotExist:
        return HTTPException(detail="Project doesn't exist!", status_code=404)

    if project.user.email != user:
        return HTTPException(detail="Project does not belong to you.", status_code=401)

    for training_class in project.classes:
        data = {
            "project": project.name,
            "username": user,
            "subclass": training_class.label,
            "search_term": training_class.search_term,
            "max_images": training_class.max_images
        }
        data = json.dumps(data)
        RedisConn.CONN.rpush('gathering-queue', data)

    return "data collection queued"