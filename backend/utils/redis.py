import redis
import os
from backend.settings import REDIS_URL

pool = redis.ConnectionPool.from_url(REDIS_URL, decode_responses=True)
redis_conn = redis.StrictRedis(connection_pool=pool)
