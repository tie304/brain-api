import uuid
import datetime
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel


class TrainingRun(EmbeddedMongoModel):
    _id = fields.CharField(required=True, default=uuid.uuid4, primary_key=True)
    training_start_time = fields.DateTimeField(default=datetime.datetime.now)
    training_end_time = fields.DateTimeField()
    epochs = fields.IntegerField()
    val_accuracy = fields.ListField()
    training_accuracy = fields.ListField()
    val_loss = fields.ListField()
    training_loss = fields.ListField()


class TrainingInstance(EmbeddedMongoModel):
    _id = fields.CharField(required=True, default=uuid.uuid4, primary_key=True)
    status = fields.CharField(default="pending_training")
    created = fields.DateTimeField(default=datetime.datetime.now())
    training_start_time = fields.DateTimeField()
    training_end_time = fields.DateTimeField()
    training_runs = fields.EmbeddedDocumentListField(TrainingRun, default=[])


