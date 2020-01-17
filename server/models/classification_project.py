from typing import List
from pydantic import BaseModel


class ClassData(BaseModel):
    label: str
    keywords: List[str]


class CreateClassificationProject(BaseModel):
    name: str
    description: str
    classes: List[ClassData]


class GetClassificationProject(BaseModel):
    name: str
    description: str
    classes: List[ClassData]

class UpdateClassificationProject(BaseModel):
    name: str
    description: str
    classes: List[ClassData]


class GetClassificationProjects(BaseModel):
    projects: List[GetClassificationProject]