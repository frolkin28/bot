import redis
import typing

from application.entities import DriverEntity

import config


class DriversQueueService:
    def __init__(self):
        self._client = redis.Redis(**config.redis_config)

    def push(self, telegram_id: int) -> None:
        self._client.rpush(config.REDIS_QUEUE_NAME, telegram_id)

    def pop(self) -> typing.Optional[int]:
        telegram_id = self._client.lpop(config.REDIS_QUEUE_NAME)
        if telegram_id:
            return int(telegram_id.decode('utf-8'))
        else:
            return None

    def remove(self, telegram_id: int) -> bool:
        return bool(self._client.lrem(config.REDIS_QUEUE_NAME, 0, telegram_id))

    # method for testing
    def get_all(self):
        return self._client.lrange(config.REDIS_QUEUE_NAME, 0, -1)
