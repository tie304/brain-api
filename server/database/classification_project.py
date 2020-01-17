import uuid
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel


from database.user import User
from database.training import TrainingInstance
from database.gathering import GatheringRun


class ClassData(EmbeddedMongoModel):
    label = fields.CharField(required=True)
    keywords = fields.ListField()


class ClassificationProject(MongoModel):
    _id = fields.CharField(required=True, default=uuid.uuid4(), primary_key=True)
    user = fields.ReferenceField(User, required=True)
    name = fields.CharField(required=True, blank=False)
    created = fields.DateTimeField(required=True)
    description = fields.CharField()
    classes = fields.EmbeddedDocumentListField(ClassData, default=[])
    training_instances = fields.EmbeddedDocumentListField(TrainingInstance, default=[])
    data_gathering_runs = fields.EmbeddedDocumentListField(GatheringRun, default=[])