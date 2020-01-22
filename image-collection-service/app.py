import os
import sys
import json
import datetime
import pymodm.errors as DBerrors
from redis_conn import RedisConn
from src.image_collector import GoogleImageCollector
from pymodm import connect
from database.classification_project import ClassificationProject
from database.gathering import GatheringRun


RedisConn.initialize(os.environ.get("REDIS_HOST"), os.environ.get("REDIS_PORT"))
connect(os.environ.get('MONGO_URI') + os.environ.get("MONGO_DB_NAME"))

data = RedisConn.CONN.blpop('gathering-queue') # blocking operation until data enters queue
gathering_data = json.loads(data[1]) # load json string from redis

try:
    project = ClassificationProject.objects.get({'name': gathering_data.get('project')})
except DBerrors.DoesNotExist:
    sys.exit(1)

# build a list of previously visited urls for project
visited_urls = []
for run in project.data_gathering_runs:
    visited_urls = visited_urls + run.urls_visited

run = GatheringRun(search_term=gathering_data.get('search_term'))
run.status = "collecting_data"
project.data_gathering_runs.append(run)
project.save()


collector = GoogleImageCollector(project=gathering_data.get('project'),
                                 subclass = gathering_data.get('subclass'),
                                 search_term = gathering_data.get('search_term'),
                                 max_images=gathering_data.get('max_images'),
                                 username=gathering_data.get('username'),
                                 visited_urls=visited_urls)

image_urls = collector.collect_images()

try:
    run.end_time = datetime.datetime.now()
    run.urls_visited = image_urls
    run.status = "collection_complete"
    project.save()
except Exception as e:
    print(e)
    sys.exit(1)

sys.exit(0)
