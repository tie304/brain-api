import uuid
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel


class GatheringRun(MongoModel):
    start_time = fields.DateTimeField(required=True)
    end_time = fields.DateTimeField(required=True)
    images_gathered = fields.IntegerField()
    keyword_searched = fields.CharField()
    urls_visited = fields.ListField()


