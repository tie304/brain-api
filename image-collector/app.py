import json
from redis_conn import RedisConn
from src.image_collector import  GoogleImageCollector

RedisConn.initialize('redis', 6379)

data = RedisConn.CONN.blpop('gathering-queue') # blocking operation until data enters queue
gathering_data = json.loads(data[1]) # load json string from redis

print(gathering_data.get('max_images'))

collector = GoogleImageCollector(project=gathering_data.get('project'),
                                 subclass = gathering_data.get('subclass'),
                                 search_term = gathering_data.get('search_term'),
                                 max_images=gathering_data.get('max_images'), username=gathering_data.get('username'))

collector.collect_images()
