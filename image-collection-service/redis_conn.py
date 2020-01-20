import redis


class RedisConn:
    CONN = None
    @staticmethod
    def initialize(host, port):
        RedisConn.CONN = redis.Redis(
            host=host,
            port=port)
