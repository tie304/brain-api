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


class GatheringRun(BaseModel):
    id: str = Field(..., alias='_id')
    start_time: datetime.datetime
    status: str
    end_time: datetime.datetime = None
    search_term: str
    urls_visited: list = []


class ClassData(BaseModel):
    label: str
    search_term: str
    max_images: int = 1000


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
    data_gathering_runs: List[GatheringRun] = []


class UpdateClassificationProject(BaseModel):
    name: str
    description: str
    classes: List[ClassData]


class GetClassificationProjects(BaseModel):
    projects: List[GetClassificationProject]