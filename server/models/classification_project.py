from typing import List, Any
import datetime
from pydantic import BaseModel, Field




class TrainingRuns(BaseModel):
    id: str = Field(..., alias='_id')
    training_start_time: datetime.datetime
    training_end_time: Any
    epochs: int
    val_accuracy: Any
    training_accuracy: list
    val_loss: list
    training_loss: list


class TrainingInstance(BaseModel):
    id: str = Field(..., alias='_id')
    status: Any
    created: datetime.datetime
    training_runs: List[TrainingRuns] = []


class ClassData(BaseModel):
    label: str
    search_term: str


class CreateClassificationProject(BaseModel):
    name: str
    description: str
    classes: List[ClassData]


class GetClassificationProject(BaseModel):
    id: str = Field(..., alias='_id')
    name: str
    description: str
    classes: List[ClassData]
    training_instances: List[TrainingInstance] = []


class UpdateClassificationProject(BaseModel):
    name: str
    description: str
    classes: List[ClassData]


class GetClassificationProjects(BaseModel):
    projects: List[GetClassificationProject]