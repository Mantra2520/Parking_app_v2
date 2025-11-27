import redis

redis_auth = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

redis_cach = redis.Redis(
    host="localhost",
    port=6379,
    db=1,
    decode_responses=True
)