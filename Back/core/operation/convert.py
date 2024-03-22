import json
from core.config import redis, setting


async def add_to_redis(user_data: dict, name: str):
    user_str = json.dumps(user_data)
    await redis.set(name=name, value=user_str, ex=setting.EX)


async def get_to_redis(key: str) -> dict:
    item = await redis.get(key)
    return json.loads(item)
