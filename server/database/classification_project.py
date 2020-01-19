import uuid
import datetime
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel


from database.user import User
from database.training import TrainingInstance
from database.gathering import GatheringRun


class ClassData(EmbeddedMongoModel):
    label = fields.CharField(required=True)
    keywords = fields.ListField()


class ClassificationProject(MongoModel):
    _id = fields.CharField(primary_key=True, required=True, default=uuid.uuid4)
    user = fields.ReferenceField(User, required=True)
    name = fields.CharField(required=True, blank=False)
    created = fields.DateTimeField(required=True, default=datetime.datetime.now())
    description = fields.CharField()
    classes = fields.EmbeddedDocumentListField(ClassData, default=[])
    training_instances = fields.EmbeddedDocumentListField(TrainingInstance, default=[])
    data_gathering_runs = fields.EmbeddedDocumentListField(GatheringRun, default=[])