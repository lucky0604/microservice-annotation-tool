from aioredis import create_redis_pool, Redis


async def get_redis_pool() -> Redis:
    # redis = await create_redis_pool(f'redis://host.docker.internal:6379/0?encoding=utf-8')
    redis = await create_redis_pool('', password='')
    return redis
