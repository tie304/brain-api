import json
import pymodm.errors as DBerrors
from fastapi import APIRouter, HTTPException, Depends
from redis_conn import RedisConn
from modules.auth import oauth2_scheme
from modules.auth import validate_current_user
from database.classification_project import ClassificationProject
from database.training import TrainingInstance


ERRORS = {
    "NO_PROJECT": "Sorry that project doesn't exist",
    "ALREADY_TRAINING": "You already have a model training or pending. Please wait until the current training process is finished"
}

router = APIRouter()


@router.post("/train/", status_code=201, tags=["trainer"])
async def collect(_id: str, token: str = Depends(oauth2_scheme)):
    username = await validate_current_user(token)
    try:
        project_db = ClassificationProject.objects.get({'_id': _id})
    except DBerrors.DoesNotExist:
        return HTTPException(detail=ERRORS.get('NO_PROJECT'), status_code=400)

    try:
        if project_db.user.email != username:
            raise ValueError(ERRORS.get('NO_PROJECT'))
        for instance in project_db.training_instances:
            if instance.status == "pending_training" or instance.status == "training":
                raise ValueError(ERRORS.get("ALREADY_TRAINING"))
    except ValueError as e:
        return HTTPException(detail=str(e), status_code=400)

    training_instance = TrainingInstance()
    project_db.training_instances.append(training_instance)
    project_db.save()


    data = {
        "project_id": project_db._id,
        "project_name": project_db.name,
        "training_instance_id": training_instance._id,
        "username": username,
    }

    data = json.dumps(data)
    RedisConn.CONN.rpush('training-queue', data)

    return "your training job as queued"