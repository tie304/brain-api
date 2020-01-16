from database.user import User
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel


class TrainingRun(EmbeddedMongoModel):
    training_start_time = fields.DateTimeField(required=True)
    training_end_time = fields.DateTimeField(required=True)
    val_accurcay = fields.CharField(required=True, blank=False)
    training_accuracy = fields.CharField(required=True, blank=False)
    val_loss = fields.CharField(required=True, blank=False)
    training_loss = fields.CharField(required=True, blank=False)
    run_parameters = fields.DictField()
    images_removed = fields.IntegerField()


class TrainingInstance(EmbeddedMongoModel):
    training_start_time = fields.DateTimeField(required=True)
    training_end_time = fields.DateTimeField(required=True)
    training_runs = fields.EmbeddedDocumentListField(TrainingRun, default=[])


