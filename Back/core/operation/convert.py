import json
from core.config import redis, setting


async def add_to_redis(user_data: dict, name: str):
    user_str = json.dumps(user_data)
    await redis.set(name=name, value=user_str, ex=setting.EX)


async def get_user_redis(key: str) -> dict:
    user_str = await redis.get(key)
    return json.loads(user_str)
