import uuid
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel


class GatheringRun(MongoModel):
    _id = fields.CharField(required=True, default=uuid.uuid4, primary_key=True)
    start_time = fields.DateTimeField()
    end_time = fields.DateTimeField()
    images_gathered = fields.IntegerField()
    keyword_searched = fields.ListField()
    urls_visited = fields.ListField()



