import uuid
import datetime
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel


class GatheringRun(MongoModel):
    _id = fields.CharField(required=True, default=uuid.uuid4, primary_key=True)
    start_time = fields.DateTimeField(default=datetime.datetime.now)
    status = fields.CharField()
    end_time = fields.DateTimeField()
    search_term = fields.CharField()
    urls_visited = fields.ListField(default=[], blank=True)



