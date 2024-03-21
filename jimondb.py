from peewee import *

from loguru import logger

_db = SqliteDatabase("jimon.db")


class TableUpdate(Model):
    update_type = IntegerField()
    hostname = CharField()
    timestamp = IntegerField()
    temp = FloatField()
    cpu_usage = FloatField()
    mem_usage = FloatField()

    class Meta:
        database = _db


def connect():
    _db.connect()
    _db.create_tables([TableUpdate], safe=True)


def insert(
    update_type: int,
    hostname: str,
    timestamp: int,
    temp: float,
    cpu_usage: float,
    mem_usage: float,
):
    with _db.atomic():
        TableUpdate.create(
            update_type=update_type,
            hostname=hostname,
            timestamp=timestamp,
            temp=temp,
            cpu_usage=cpu_usage,
            mem_usage=mem_usage,
        )
        logger.debug(
            f"{update_type=} {hostname=} {timestamp=} {temp=} {cpu_usage=} {mem_usage=}"
        )


def query_all():
    return TableUpdate.select()


def debug():
    for update in query_all():
        logger.debug(
            f"{update.update_type=} {update.hostname=} {update.timestamp=} {update.temp=} {update.cpu_usage=} {update.mem_usage=}"
        )


def close():
    _db.close()


if __name__ == "__main__":
    connect()
    debug()
    close()
